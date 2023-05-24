for ($i = 1; $i -le 15; $i++) {
    python main.py -sf Primary2.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary3.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary5.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary6.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary7.wav -sn PRT -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
}


for ($i = 1; $i -le 15; $i++) {
    python main.py -sf Primary1.wav -sn VTL -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary2.wav -sn VTL -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary3.wav -sn VTL -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary4.wav -sn VTL -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary5.wav -sn VTL -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary6.wav -sn VTL -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary7.wav -sn VTL -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
    python main.py -sf Primary8.wav -sn VTL -ps 75 -gs 40 -el 2 -mr 0.1 -sd 0.2 -sl exponential -cr one_point -fr cent -dm SAD -id $i --sub_directory chapter_5_ii\multi_model_comparison
}
