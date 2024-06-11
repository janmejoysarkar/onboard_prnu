Nov 24 2023 

PRNU measurement results

355nm LED
Data: 2023-05-31_4_led_355nm_p75_current_10_times_100ms_fw1_04_fw2_07_005
odd numbered files
PRNU_full_frame %=  0.7642755180711547
PRNU % [e,f,g,h]=  [0.76026561 0.77045962 0.78199399 0.74373783]

even numbered files
PRNU_full_frame %=  0.7782287820285444
PRNU % [e,f,g,h]=  [0.76788199 0.78476329 0.78769589 0.77228013]


255 nm LEDs
odd numbered files-
PRNU_full_frame %=  0.8456534280824852
PRNU % [e,f,g,h]=  [0.83570837 0.81294152 0.89547517 0.83604228]

even numbered files-
PRNU_full_frame %=  0.8569270509414467
PRNU % [e,f,g,h]=  [0.84244532 0.83282348 0.90060421 0.85003404]


355nm- 11 px kernel used.
calib_stats(single_355, corrected_355, prnu_355, 2500, 2500, 25)

**** 355 nm flat stats ****
[1] Sdev Raw: 0.007624302681348463
[2] Sdev Corrected: 0.0043166284139267526
[3] Sdev PRNU:  0.00614391673907794
[4] sqrt(Raw^2-PRNU^2):  0.004514673684785564
Upon good FF correction, [2] and [4] should match well

calib_stats(single_255, corrected_255, prnu_255, 1000, 2500, 25)

255nm- 13 px kernel used.
**** 255 nm flat stats ****
[1] Sdev Raw: 0.007769254772228668
[2] Sdev Corrected: 0.0033225724347596347
[3] Sdev PRNU:  0.007196172419475341
[4] sqrt(Raw^2-PRNU^2):  0.0029285529233702336
Upon good FF correction, [2] and [4] should match well

NOTE: The values for 2 and 4 do not always match for different crop locations
and areas.(base)







