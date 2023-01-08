for ($i = 1; $i -le 100; $i++) {
    python main.py -sf Primary1.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr hz -dm SAD -id $i --sub_directory chapter_4\change_in_standard_deviation
}