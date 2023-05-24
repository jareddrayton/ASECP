$sds = @('0.1', '0.2', '0.3')

foreach ( $sd in $sds ) {
    for ($i = 1; $i -le 15; $i++) {
        python main.py -sf Primary1.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.05 -sd $sd -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
        python main.py -sf Primary4.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.05 -sd $sd -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
        python main.py -sf Primary8.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.05 -sd $sd -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
    }
}

foreach ( $sd in $sds ) {
    for ($i = 1; $i -le 15; $i++) {
        python main.py -sf Primary1.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.15 -sd $sd -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
        python main.py -sf Primary4.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.15 -sd $sd -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
        python main.py -sf Primary8.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.15 -sd $sd -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
    }
}

for ($i = 1; $i -le 15; $i++) {
    python main.py -sf Primary1.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.1 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
    python main.py -sf Primary4.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.1 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
    python main.py -sf Primary8.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.1 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
}

for ($i = 1; $i -le 15; $i++) {
    python main.py -sf Primary1.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.3 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
    python main.py -sf Primary4.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.3 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
    python main.py -sf Primary8.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.3 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\mutation
}