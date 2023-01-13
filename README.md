# Compression par la méthode de Huffman 

## Huffman-analyze.py : 
Ce fichier permet de trouver le nombre d'apparition de chaque lettre dans un fichier puis de créer le graphe de Huffman (code de chaque lettre). 

Paramètres possibles : 
- le nom du fichier à partir duquel on fait le code (obligatoire)
- --coder / -c : permet de choisir le nom du fichier dans lequel on enregistre le code de chaque lettre. (optionnel) 
  (les fichiers contenant le code des lettres sont sauvés dans le dossier huffman_graph par défaut et ont l'extension .coder)
- --bin / -b : permet de choisir si on veut enregistrer le fichier dans un fichier binaire ou non (optionnel)
  (par défaut le fichier enregistre en fichier texte)

## Huffman.py : 
Ce fichier permet d'encoder et décoder des fichiers (compréssion). 

Paramètres possibles :  
- --decode / -d : si l'argument est passé on décode, sinon on encode. 
- --output / -o : permet de choisir le nom du fichier dans lequel on enregistre la sortie. (optionnel) 
  (par défaut on sauve les fichiers encodés dans le dossier output/huf avec un .huf et on décode dans le dossier output/decoded)
- --coder / -c : permet de choisir le graphe de Huffman utilisé pour encoder / decoder (optionnel)
  (par défaut celui utilisé est huffman_graph/english.txt)
- --huff_graph_bin / -hufb : nécessaire si on choisit un autre graphe de Huffman que celui par défault et que le graphe choisit est stocké dans un fichier bianire
- --bin / - b : permet de choisir si on veut encoder en binaire / si on décode un fichier binaire (cette fois-ci on parle du fichier encoder/décoder et non du décodage du graphe). 