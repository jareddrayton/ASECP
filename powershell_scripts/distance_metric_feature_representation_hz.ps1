$i=1
for(;$i -le 15;$i++)
{
    python main.py -sf Primary1.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm SAD -id $i
    python main.py -sf Primary4.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm SAD -id $i
    python main.py -sf Primary8.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm SAD -id $i
}

$i=1
for(;$i -le 15;$i++)
{
    python main.py -sf Primary1.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm EUC -id $i
    python main.py -sf Primary4.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm EUC -id $i
    python main.py -sf Primary8.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm EUC -id $i
}

$i=1
for(;$i -le 15;$i++)
{
    python main.py -sf Primary1.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm SSD -id $i
    python main.py -sf Primary4.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm SSD -id $i
    python main.py -sf Primary8.wav -sn PRT -ps 150 -gs 20 -el 2 -mr 0.1 -sd 0.2 -sl exponential -fr hz -dm SSD -id $i
}