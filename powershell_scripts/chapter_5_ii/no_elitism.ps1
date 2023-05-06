for ($i = 1; $i -le 15; $i++) {
    python main.py -sf Primary1.wav -sn PRT -ps 150 -gs 20 -el 0 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\no_elitism
    python main.py -sf Primary4.wav -sn PRT -ps 150 -gs 20 -el 0 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\no_elitism
    python main.py -sf Primary8.wav -sn PRT -ps 150 -gs 20 -el 0 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\no_elitism
}
