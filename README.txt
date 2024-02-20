Fonctionnalités implémentées :

	Les noms de variables à plusieurs caractères, nous pouvons faire des opérations avec ces variables 
	(Exemple : test=2;print(test+6);)
	
	Nous pouvons les affecter 
	(Exemple : x=2;)
	
	Les conditions, avec If, If Else 
	(Exemple : if(i<10){ print(i); };)
	
	Les boucles : While, For 
	(Exemple : while(i<10) { i++; };)
	(Exemple : for(i=0;i<10;i++) { print(i); };)
	
	Affichage de l'arbre
		Pour l'affectation : "assign"				Enfants : "NomVariable" et "Valeur"
		Pour le if : "if"					Enfants : "Condition" et "bloc" ou "Condition", "bloc" et "else"
		Pour le while : "while"					Enfants : "Condition" et "bloc"
		Pour le for : "for"					Enfants : "Affectation", "Condition" et "Incrementation"
		Pour la declaration void : "VoidDeclaration"		Enfants : "TypeFonction" et "NomFonction" ou "TypeFonction", "NomFonction" et "Paramètres"
		Pour la declaration function : "FunctionDeclaration"	Enfants : "TypeFonction", "NomFonction" et "Retour" ou "TypeFonction", "NomFonction", "Paramètres" et "Retour"
		Pour l'appel fonction : "call"				Enfants : "TypeFonction", "NomFonction" et "bloc" ou "TypeFonction","NomFonction", "Paramètres" et "bloc"
		Pour le bloc : "bloc"					Enfants : "bloc" et "Vide" ou "bloc" et "bloc"
		Pour les paramètres : "Param"				Enfants : "NomVariable" ou "Expression"
		Pour le print : "print"					Enfants : "Expression"
	
	Les fonctions void 
	(Exemple declaration : void test(x,y) { print(x); print(y); };)
	(Exemple appel : test(10+6,5-2);)
	
	L'incrémentation de variable 
	(Exemple : x++;)