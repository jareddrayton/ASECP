for ($i = 1; $i -le 15; $i++) {
    python main.py -sf Primary1.wav -sn PRT -ps 300 -gs 10 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\pop_gen_size
    python main.py -sf Primary4.wav -sn PRT -ps 300 -gs 10 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\pop_gen_size
    python main.py -sf Primary8.wav -sn PRT -ps 300 -gs 10 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\pop_gen_size
}

for ($i = 1; $i -le 15; $i++) {
    python main.py -sf Primary1.wav -sn PRT -ps 100 -gs 30 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\pop_gen_size
    python main.py -sf Primary4.wav -sn PRT -ps 100 -gs 30 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\pop_gen_size
    python main.py -sf Primary8.wav -sn PRT -ps 100 -gs 30 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\pop_gen_size
}

for ($i = 1; $i -le 15; $i++) {
    python main.py -sf Primary1.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\pop_gen_size
    python main.py -sf Primary4.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\pop_gen_size
    python main.py -sf Primary8.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\pop_gen_size
}
