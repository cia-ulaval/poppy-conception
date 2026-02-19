- Vérification de max 5 volts pour le condensateur du RPi.
- La prise mâle qui doit entrer dans le SMPS est une prise de type "Jack DC male"
- Il faudra ajouter un module après la batterie. Pour s'assurer que la tension ne descende pas trop.
- [Convertisseur USB-c à Jack DC 5.5mm a 2.1 mm](https://www.amazon.ca/Female-Input-Charge-Laptop-Notebook/dp/B0BPB8BPRP/ref=asc_df_B0BPB8BPRP?mcid=e308e9a0235b3abb9996fff469dfd470&tag=googleshopc0c-20&linkCode=df0&hvadid=706760541787&hvpos=&hvnetw=g&hvrand=545519972404187833&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9000264&hvtargid=pla-2297094582176&psc=1&hvocijid=545519972404187833-B0BPB8BPRP-&hvexpln=0&gad_source=1) Utile si on a une batterie dont l'extrant aboutit sur un USB-c mâle.
- [USB à Jack DC 5.5 mm x 2.1 mm](https://www.amazon.ca/AAOTOKK-Converter-5-5%C3%972-1mm-Connector-Charging/dp/B0B1WY584Y/ref=asc_df_B0B1WY584Y?mcid=ed4babb22a6136feb32f16af2c294267&tag=googleshopc0c-20&linkCode=df0&hvadid=706724917107&hvpos=&hvnetw=g&hvrand=17230526074833737154&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9000264&hvtargid=pla-2265302851623&psc=1&hvocijid=17230526074833737154-B0B1WY584Y-&hvexpln=0&gad_source=1) 
    - Utile si on a une batterie dont l'extrant aboutit sur un USB mâle. (not so likely...)
- Batterie qui fournit entre 8 et 12 Ah (8000 mmAh, 12000 mmAh) (valeur d'énergie).
- Batterie va shooter 12V fixes. Mais la batterie peut shooter la quantité de Watts qu'on lui demande, dans les plages de valeurs fixées par notre utilisation.
- Li-on ou Lipo-pack-3s ou Life-Po4-4s
    - Li-on : [bon spécimen de 306g](https://www.amazon.ca/Rechargeable-Powerful-Portable-Suitable-Equipment/dp/B0C2Q6DXRL/ref=asc_df_B0C2Q6DXRL?mcid=d84bd3135b6734f0accbdb72b5a8be96&tag=googleshopc0c-20&linkCode=df0&hvadid=706724917116&hvpos=&hvnetw=g&hvrand=2125347016544361175&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9000264&hvtargid=pla-2312154554568&psc=1&hvocijid=2125347016544361175-B0C2Q6DXRL-&hvexpln=0&gad_source=1)
        - Problème : les dimensions et le poids affichés dans l'image sont pour du 6000 mAh... malheureusement.
    - LiPo-pack-3s
- Il nous faut un BMS. Le BMS est le module de protection dont on parlait.
- On pourrait (il serait même souhaitable) brancher deux (2) batteries en série. De cette façon, on pourra sélectionner des batteries ayant moins d'énergie stockée, et donc un volume moindre. Nous placerions deux batteries, une sur chaque flanc de Poppy.

- [Meilleur spécimen qu'on a](https://ca.lightmalls.com/12v-4000mah-18650-lithium-ion-dc-12-6v-super-rechargeable-battery-pack?ff=6&fp=7295&gad_source=1&gad_campaignid=17426280671&gbraid=0AAAAADt5-bJ4q2bdtR2RqKZJN3448fhDG&gclid=Cj0KCQiAhtvMBhDBARIsAL26pjHKWbNLTPhlK_QOtZwIEX-21fVZBIJFR5eLqMiWIMSheYQp7mQUz74aApmwEALw_wcB). 
    - Specs : 4000 mAh, 12V, 7x5x2 cm. Calcul : 38.4 minutes à elle seule à 60W. Donc pour deux batteries comme ça, ça fait 76.8 minutes !
    


| Type Batterie | Avantage | Désavantages |
| ------------- | -------- | ------------ | 
| Li-on | Le module BMS est intégré. | Charge simple.  |
| Li-Po | Plus efficace, plus compacte, plus puissante | Risques dans le chargement. Peut exploser. Pas de BMS. |

# À faire : 
- Contacter l'Université pour demander si on peut avoir des batteries [comme ceci](https://www.amazon.ca/Rechargeable-Powerful-Portable-Suitable-Equipment/dp/B0C2Q6DXRL/ref=asc_df_B0C2Q6DXRL?mcid=d84bd3135b6734f0accbdb72b5a8be96&tag=googleshopc0c-20&linkCode=df0&hvadid=706724917116&hvpos=&hvnetw=g&hvrand=2125347016544361175&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9000264&hvtargid=pla-2312154554568&psc=1&hvocijid=2125347016544361175-B0C2Q6DXRL-&hvexpln=0&gad_source=1) dans le local PLT-3778.