# distance metric, feature representation, selection operator
python main.py -sf Primary1.wav -sn VTL -ps 20 -gs 5 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm SAD -id 01
python main.py -sf Primary1.wav -sn VTL -ps 20 -gs 5 -el 2 -mr 0.1 -sd 0.2 -sl linear -fr mel -dm EUC -id 02
python main.py -sf Primary1.wav -sn VTL -ps 20 -gs 5 -el 2 -mr 0.1 -sd 0.2 -sl proportional -fr cent -dm SSD -id 03

# no elitism
python main.py -sf Primary1.wav -sn PRT -ps 20 -gs 5 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm SAD -id 04

# vocal tract lab
python main.py -sf Primary1.wav -sn VTL -ps 20 -gs 5 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm SAD -id 04





