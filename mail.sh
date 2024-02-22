#!/bin/bash

fichier_texte="./grades.txt"
fichier_excel="./fichier_sortie.xlsx"

fichier_emails="./fichier_emails.txt"

ssconvert "$fichier_texte" "$fichier_excel"

if [ ! -f "$fichier_excel" ]; then
    echo "error."
    exit 1
fi

while IFS= read -r email; do
    echo "$email..."
    mail -s "Notes du dernier examens" -a "$fichier_excel" "$email" <<< "Comme d'habitudes, me signaler si vous trouver des erreurs"
done < "$fichier_emails"

echo "Fin"
