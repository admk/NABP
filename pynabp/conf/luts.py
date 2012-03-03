import math
from itertools import chain
from pynabp.utils import bin_width_of_dec_vals
from pynabp.fixed_point_arith import FixedPoint


def shift_lut_defines(shift_accu_precision):
    fp = FixedPoint(1, shift_accu_precision, value=0)
    @fp.verilog_repr_decorator
    def lookup(angle):
        if angle < 0 or angle >= 180:
            raise ValueError('Angle must be within range 0-180')
        if (0 <= angle and angle < 45) or (135 <= angle and angle < 180):
            return abs(math.tan(math.radians(angle)))
        else:
            return abs(1 / math.tan(math.radians(angle)))
    defines = {
            'tShiftAccuBase': fp,
            'lutShiftAccuBaseFunc': lookup,
            }
    return defines

def map_lut_defines(conf):
    defines = _map_accu_part_defines(conf)
    defines.update(_map_accu_base_defines(conf))
    defines.update(_map_accu_init_defines(conf))
    return defines

def _map_accu_part_lookup(conf):
    last_pe = conf['partition_scheme']['partitions'][-1]
    i_size = conf['image_size']
    i_center = conf['image_center']
    p_center = conf['projection_line_center']

    def lookup(angle):
        sin_val = math.sin(math.radians(angle))
        cos_val = math.cos(math.radians(angle))
        if (0 <= angle and angle < 45):
            val = last_pe * cos_val
        elif (45 <= angle and angle < 90):
            val = - last_pe * sin_val
        elif (90 <= angle and angle < 135):
            val = - last_pe * sin_val + i_size * cos_val
        elif (135 <= angle and angle < 180):
            val = last_pe * cos_val - i_size * sin_val
        else:
            raise RuntimeError('Invalid angle encountered')
        return val + i_center * sin_val - i_center * cos_val + p_center

    return lookup

def _map_accu_base_lookup(angle):
    if ((0 <= angle and angle < 45) or
        (135 <= angle and angle < 180)):
        return -math.cos(math.radians(angle))
    elif (45 <= angle and angle < 135):
        return math.sin(math.radians(angle))
    else:
        raise RuntimeError('Invalid angle encountered')

def _map_accu_part_defines(conf):
    """Define *MapAccuPart constants
    """
    # generate lookup table
    lut_map_accu_part = map(_map_accu_part_lookup(conf), xrange(0, 180))

    # evaluate bit lengths for the lookup table values
    accu_part_int_len, accu_part_signed = bin_width_of_dec_vals(
            lut_map_accu_part)

    defines = {
            'lutMapAccuPart': lut_map_accu_part,
            'tLUTMapAccuPart': FixedPoint(
                accu_part_int_len, conf['kMapAccuPartPrecision'],
                accu_part_signed),
            'tMapAccuPart': FixedPoint(
                accu_part_int_len, conf['kMapAccuPrecision'],
                accu_part_signed)
            }
    return defines

def _map_accu_base_defines(conf):
    """Define *MapAccuBase constants
    """
    defines = {
            'tMapAccuBase': FixedPoint(1, conf['kMapAccuPrecision'], True),
            'lutMapAccuBase': map(_map_accu_base_lookup, xrange(0, 180))
            }
    return defines

def _map_accu_init_defines(conf):
    """Define *MapAccuInit constants
    """
    # range required for accu_init
    def accu_init_vals(angle):
        part_val = _map_accu_part_lookup(conf)(angle)
        line_val = -conf['partition_scheme']['size'] * \
                _map_accu_base_lookup(angle)
        return (part_val, part_val + line_val)
    def accu_init_range():
        accu_init_range_list = map(accu_init_vals, xrange(0, 180))
        accu_init_range_list = list(chain.from_iterable(accu_init_range_list))
        return bin_width_of_dec_vals(accu_init_range_list)
    # range for accumulated value
    def accu_vals(angle):
        scan_val = conf['image_size'] * _map_accu_base_lookup(angle)
        val_0, val_1 = accu_init_vals(angle)
        return (val_0, val_1, val_0 + scan_val, val_1 + scan_val)
    def accu_range():
        accu_range_list = map(accu_vals, xrange(0, 180))
        accu_range_list = list(chain.from_iterable(accu_range_list))
        return bin_width_of_dec_vals(accu_range_list)

    init_len, init_signed = accu_init_range()
    accu_len, accu_signed = accu_range()
    accu_prec = conf['kMapAccuPrecision']
    defines = {
            'tMapAccuInit': FixedPoint(init_len, accu_prec, init_signed),
            'tMapAccu': FixedPoint(accu_len, accu_prec, init_signed)
            }
    return defines
