onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -expand -group global -format Logic /NABPFilteredRAMTest/clk
add wave -noupdate -expand -group global -format Logic /NABPFilteredRAMTest/reset
add wave -noupdate -expand -group host -format Literal /NABPFilteredRAMTest/hs_angle
add wave -noupdate -expand -group host -format Logic /NABPFilteredRAMTest/hs_next_angle_ack
add wave -noupdate -expand -group host -format Logic /NABPFilteredRAMTest/hs_has_next_angle
add wave -noupdate -expand -group host -format Literal -radix unsigned /NABPFilteredRAMTest/hs_s_val
add wave -noupdate -expand -group host -format Literal /NABPFilteredRAMTest/filter_out
add wave -noupdate -expand -group swappable -format Logic -radix decimal /NABPFilteredRAMTest/hs_next_angle
add wave -noupdate -expand -group swappable -format Literal /NABPFilteredRAMTest/filtered_ram_swap_control_uut/state
add wave -noupdate -expand -group swappable -format Literal /NABPFilteredRAMTest/filtered_ram_swap_control_uut/next_state
add wave -noupdate -expand -group swappable -format Logic /NABPFilteredRAMTest/filtered_ram_swap_control_uut/fill_done
add wave -noupdate -expand -group swappable -format Logic /NABPFilteredRAMTest/filtered_ram_swap_control_uut/fill_kick
add wave -noupdate -expand -group swappable -format Logic /NABPFilteredRAMTest/filtered_ram_swap_control_uut/swap
add wave -noupdate -expand -group swappable -format Logic /NABPFilteredRAMTest/filtered_ram_swap_control_uut/sw_sel
add wave -noupdate -expand -group pr_ver -format Logic /NABPFilteredRAMTest/filtered_ram_swap_control_uut/pr_next_angle_ack
add wave -noupdate -expand -group pr_ver -format Logic /NABPFilteredRAMTest/filtered_ram_swap_control_uut/pr_next_angle
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {75736 ns} 0}
configure wave -namecolwidth 162
configure wave -valuecolwidth 69
configure wave -justifyvalue left
configure wave -signalnamewidth 1
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {73636 ns} {82916 ns}

run -all
