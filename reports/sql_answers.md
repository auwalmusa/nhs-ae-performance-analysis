# SQL Analysis Answers

## Q1: National monthly trend and the January dip

| month               |   attendances |   perf_pct |   perf_change_vs_prev_month |   dta_12hr_waits |
|:--------------------|--------------:|-----------:|----------------------------:|-----------------:|
| 2025-10-01 00:00:00 |   1.44948e+06 |       59.9 |                       nan   |            54326 |
| 2025-11-01 00:00:00 |   1.42003e+06 |       60.1 |                         0.2 |            50648 |
| 2025-12-01 00:00:00 |   1.40764e+06 |       59.3 |                        -0.8 |            50789 |
| 2026-01-01 00:00:00 |   1.40504e+06 |       57   |                        -2.3 |            71517 |
| 2026-02-01 00:00:00 |   1.27183e+06 |       59.1 |                         2.1 |            54649 |
| 2026-03-01 00:00:00 |   1.45101e+06 |       63.9 |                         4.8 |            46665 |

## Q2: Trusts that deteriorated most into January (min 3,000 Jan attendances)

| org_name                                                              | region                      |   perf_oct |   perf_jan |   perf_mar |   winter_deterioration |   recovery |
|:----------------------------------------------------------------------|:----------------------------|-----------:|-----------:|-----------:|-----------------------:|-----------:|
| CHESTERFIELD ROYAL HOSPITAL NHS FOUNDATION TRUST                      | NHS ENGLAND MIDLANDS        |       46.1 |       27.1 |       55   |                  -19   |       27.9 |
| HAMPSHIRE HOSPITALS NHS FOUNDATION TRUST                              | NHS ENGLAND SOUTH EAST      |       54.1 |       42   |       50.7 |                  -12.1 |        8.7 |
| WRIGHTINGTON, WIGAN AND LEIGH TEACHING HOSPITALS NHS FOUNDATION TRUST | NHS ENGLAND NORTH WEST      |       55.9 |       45.2 |       57.5 |                  -10.7 |       12.3 |
| MID AND SOUTH ESSEX NHS FOUNDATION TRUST                              | NHS ENGLAND EAST OF ENGLAND |       66.8 |       56.5 |       59.8 |                  -10.3 |        3.3 |
| ROYAL CORNWALL HOSPITALS NHS TRUST                                    | NHS ENGLAND SOUTH WEST      |       54.1 |       45.1 |       51.1 |                   -9   |        6   |
| EAST AND NORTH HERTFORDSHIRE TEACHING NHS TRUST                       | NHS ENGLAND EAST OF ENGLAND |       50.8 |       41.8 |       50.9 |                   -9   |        9.1 |
| COUNTESS OF CHESTER HOSPITAL NHS FOUNDATION TRUST                     | NHS ENGLAND NORTH WEST      |       54.2 |       45.3 |       49.1 |                   -8.9 |        3.8 |
| MILTON KEYNES UNIVERSITY HOSPITAL NHS FOUNDATION TRUST                | NHS ENGLAND EAST OF ENGLAND |       59   |       50.4 |       67.1 |                   -8.6 |       16.7 |
| SOMERSET NHS FOUNDATION TRUST                                         | NHS ENGLAND SOUTH WEST      |       53.1 |       44.5 |       52.1 |                   -8.6 |        7.6 |
| LONDON NORTH WEST UNIVERSITY HEALTHCARE NHS TRUST                     | NHS ENGLAND LONDON          |       50.9 |       42.4 |       66.7 |                   -8.5 |       24.3 |

## Q3: Regional winter deterioration

| region                               |   perf_oct |   perf_jan |   perf_mar |   winter_deterioration |
|:-------------------------------------|-----------:|-----------:|-----------:|-----------------------:|
| NHS ENGLAND SOUTH WEST               |       56.7 |       52.9 |       57.3 |                   -3.8 |
| NHS ENGLAND SOUTH EAST               |       62.5 |       58.9 |       65.8 |                   -3.6 |
| NHS ENGLAND EAST OF ENGLAND          |       62   |       58.5 |       64.9 |                   -3.5 |
| NHS ENGLAND NORTH EAST AND YORKSHIRE |       60.7 |       57.7 |       66   |                   -3   |
| NHS ENGLAND MIDLANDS                 |       57.7 |       54.9 |       62.7 |                   -2.8 |
| NHS ENGLAND LONDON                   |       62   |       59.6 |       66.6 |                   -2.4 |
| NHS ENGLAND NORTH WEST               |       57   |       55.7 |       61.3 |                   -1.3 |

## Q4: Concentration of January 12-hour DTA waits

| org_name                                                       | region                 |   dta_12hr_waits |   pct_of_national |   cumulative_pct |
|:---------------------------------------------------------------|:-----------------------|-----------------:|------------------:|-----------------:|
| ROYAL FREE LONDON NHS FOUNDATION TRUST                         | NHS ENGLAND LONDON     |             2508 |               3.5 |              3.5 |
| UNIVERSITY HOSPITALS BIRMINGHAM NHS FOUNDATION TRUST           | NHS ENGLAND MIDLANDS   |             2076 |               2.9 |              6.4 |
| NORTHERN CARE ALLIANCE NHS FOUNDATION TRUST                    | NHS ENGLAND NORTH WEST |             1610 |               2.3 |              8.7 |
| THE SHREWSBURY AND TELFORD HOSPITAL NHS TRUST                  | NHS ENGLAND MIDLANDS   |             1601 |               2.2 |             10.9 |
| UNITED LINCOLNSHIRE TEACHING HOSPITALS NHS TRUST               | NHS ENGLAND MIDLANDS   |             1595 |               2.2 |             13.1 |
| UNIVERSITY HOSPITALS OF DERBY AND BURTON NHS FOUNDATION TRUST  | NHS ENGLAND MIDLANDS   |             1544 |               2.2 |             15.3 |
| LIVERPOOL UNIVERSITY HOSPITALS NHS FOUNDATION TRUST            | NHS ENGLAND NORTH WEST |             1485 |               2.1 |             17.4 |
| WORCESTERSHIRE ACUTE HOSPITALS NHS TRUST                       | NHS ENGLAND MIDLANDS   |             1431 |               2   |             19.4 |
| EAST LANCASHIRE HOSPITALS NHS TRUST                            | NHS ENGLAND NORTH WEST |             1407 |               2   |             21.3 |
| PORTSMOUTH HOSPITALS UNIVERSITY NHS TRUST                      | NHS ENGLAND SOUTH EAST |             1400 |               2   |             23.3 |
| BARKING, HAVERING AND REDBRIDGE UNIVERSITY HOSPITALS NHS TRUST | NHS ENGLAND LONDON     |             1361 |               1.9 |             25.2 |
| BARTS HEALTH NHS TRUST                                         | NHS ENGLAND LONDON     |             1352 |               1.9 |             27.1 |
| UNIVERSITY HOSPITALS OF NORTH MIDLANDS NHS TRUST               | NHS ENGLAND MIDLANDS   |             1264 |               1.8 |             28.9 |
| EAST KENT HOSPITALS UNIVERSITY NHS FOUNDATION TRUST            | NHS ENGLAND SOUTH EAST |             1208 |               1.7 |             30.5 |
| UNIVERSITY HOSPITALS SUSSEX NHS FOUNDATION TRUST               | NHS ENGLAND SOUTH EAST |             1196 |               1.7 |             32.2 |

## Q5: Does attendance volume explain the January deterioration?

|   trusts |   avg_attendance_change_pct |   avg_perf_change_pts |   corr_volume_change_vs_perf_change |
|---------:|----------------------------:|----------------------:|------------------------------------:|
|      121 |                        -1.5 |                    -3 |                               0.004 |
