
from typing import Optional



class AlphaSequence:
    '''
    AlphaSequence est une classe générant un identifiant unique.
    
    Chaque objet AlphaSequence permet de créer un nombre entier unique dans 
    sa séquence. Le nombre généré est configurable à la construction selon 
    ces paramètres :
        - valeur de départ, 0 par défaut
        - valeur d'incrément, 1 par défaut
        - avec gestion d'une valeur maximum :
            - avec ou sans valeur maximum, sans par défaut
            - génération cyclique ou non, non par défaut
        
    La séquence est aussi disponible sous forme de chaîne de caractères. 
    Plusieurs options de formatage sont aussi possibles:
        - préfixe, une chaîne vide par défaut
        - suffixe, une chaîne vide par défaut
        - remplissage :
            - longueur, 0 par défaut 
            - caractère, '0' par défaut
        - conversion du nombre entier en texte :
            - la base de conversion, 10 par défaut
            - série de caractères à utiliser, '0123456789' par défaut
    
    Cette classe reproduit en grande partie le comportement d'une séquence du 
    langage SQL (Oracle, PostgreSql, ...). Ces quelques précisions sont 
    nécessaires :
        - Avec SQL, l'appel de 'next_value' génère la première valeur.
        - Un appel à 'current_value' avant un premier appel à 'next_value' 
          génère une erreur.
        - AlphaSequence permet optionnellement la génération de la première 
          valeur à la contruction. Voir 'generate_first'.
    
    Tous les paramètres sont définis à la création de l'objet et sont non 
    modifiables par la suite.
    '''

    class ASException(Exception):
        def __init__(self, message: str = ''):
            super().__init__('AlphaSequence.Exception : ' + message)

    def __init__(self
                , initial_value : int = 0
                , increment_by : int = 1
                , /
                , maximum_value : Optional[int] = None
                , is_cyclic : Optional[bool] = False
                , generate_first : bool = False
                , *
                , prefix : str = ''
                , suffix : str = ''
                , padding_size : int = 0
                , padding_char : str = '0'
                , conversion_chars : str = '0123456789'
                ):
        '''Crée un objet AlphaSequence.
        
        Paramètres:
            - initial_value (int) : la valeur initiale, defaut 0
            - increment_by (int) : la valeur d'incrément, defaut 1
            - maximum_value (Optional[int]) : la valeur maximum, default None
            - is_cyclic (Optional[bool]) : si la séquience est cyclique, default false
            - generate_first (bool) : si on génère la première valeur, default False
            - prefix (str) : le préfixe, defaut ''
            - suffix (str) : le suffixe, defaut ''
            - padding_size (int) : la taille de remplissage, defaut 0
            - padding_char (str) : le caractère de remplissage, defaut 0
            - conversion_chars (str) : les caractères et la base de conversion, default '0123456789'
        '''
        # inputs validation
        if not isinstance(initial_value, int):
            raise TypeError('initial_value must be an instance of type int.')
        if not isinstance(increment_by, int):
            raise TypeError('increment_by must be an instance of type int.')
        if increment_by == 0:
            raise TypeError('increment_by cannot be 0.')

        if maximum_value is not None:
            if not isinstance(maximum_value, int):
                raise TypeError('maximum_value must be an instance of type int or None.')
            if maximum_value == initial_value:
                raise ValueError('maximum_value must be different of initial_value.')
            if increment_by > 0 and maximum_value < initial_value:
                raise ValueError('maximum_value must be greater than initial_value.')
            if increment_by < 0 and maximum_value > initial_value:
                raise ValueError('maximum_value must be smaller than initial_value.')
        if is_cyclic is not None:
            if not isinstance(is_cyclic, bool):
                raise TypeError('is_cyclic must be an instance of type bool or None.')
            if is_cyclic is True and maximum_value is None:
                raise ValueError('is_cyclic cannot be True while no maximum_value is defined.')
             
        if not isinstance(generate_first, bool):
            raise TypeError('generate_first must be an instance of type bool.')

        if not isinstance(prefix, str):
            raise TypeError('prefix must be an instance of type str.')
        if not isinstance(suffix, str):
            raise TypeError('suffix must be an instance of type str.')
        if not isinstance(padding_size, int):
            raise TypeError('padding_size must be an instance of type int.')
        if padding_size < 0:
            raise ValueError('padding_size must be greater than or equal to 0.')
        if not isinstance(padding_char, str):
            raise TypeError('padding_char must be an instance of type str.')
        if len(padding_char) != 1:
            raise ValueError('padding_char must be a single character string.')
        if not isinstance(conversion_chars, str):
            if isinstance(conversion_chars, list) or isinstance(conversion_chars, tuple):
                if not all(isinstance(value, str) for value in conversion_chars):
                    raise TypeError('conversion_chars must contains only strings.')
            else:
                raise TypeError('conversion_chars must be an instance of types : str, tuple of strings or list of strings.')
            
        if len(conversion_chars) < 2:
            raise ValueError('conversion_chars must be greater than or equal to 2.')
        if len(conversion_chars) != len(set(conversion_chars)):
            raise ValueError('conversion_chars cannot have duplicates.')

        # object members assignment
        self.__initial_value = initial_value
        self.__increment_by = increment_by
        self.__current_value = self.__initial_value - self.__increment_by
        self.__current_formatted = ''
        
        self.__prefix = prefix
        self.__suffix = suffix
        self.__padding_size = padding_size
        self.__padding_char = padding_char
        self.__conversion_chars = conversion_chars if conversion_chars else '0123456789'
        self.__conversion_base = len(self.__conversion_chars)
        self.__maximum_value = maximum_value
        self.__is_cyclic = is_cyclic
        
        # process first if required
        if generate_first:
            self.__process_next_value()

    def __int_to_str(self) -> str:
        n = abs(self.__current_value)
        m = n % self.__conversion_base
        n //= self.__conversion_base
        converted = self.__conversion_chars[m]

        while n > 0:
            m = n % self.__conversion_base
            n //= self.__conversion_base
            converted = self.__conversion_chars[m] + converted

        if self.__current_value < 0:
            converted = '-' + converted

        return converted

    def __manage_maximum_value(self):
        if self.__maximum_value:
            maximum_reached =   self.__current_value > self.__maximum_value\
                                if self.__increment_by > 0\
                                else self.__current_value < self.__maximum_value

            if maximum_reached:
                if self.__is_cyclic:
                    self.__current_value = self.__initial_value
                else:
                    raise AlphaSequence.ASException('Maximum sequence value reached : {self.__maximum_value}')
        
    def __process_next_value(self) -> None:
        self.__current_value += self.__increment_by
        self.__manage_maximum_value()
        self.__current_formatted = f'{self.__prefix}{self.__int_to_str():{self.__padding_char}>{self.__padding_size}}{self.__suffix}'
        
    @property
    def initial_value(self) -> int:
        '''La valeur initiale correspond à la première valeur de la séquence.
        
        De plus, si la séquence est cyclique, c'est la valeur qui sera 
        attribuée lorsque la valeur maximum est atteinte.'''
        return self.__initial_value
    
    @property
    def increment_by(self) -> int:
        '''La valeut d'incrément correspond à la différence entre deux valeurs
        de la séquence.'''
        return self.__increment_by
    
    @property
    def maximum_value(self) -> Optional[int]:
        '''La valeur maximum est la valeur maximum autorisée.
        
        Cette valeur est la limite non incluse à laquelle la séquence adopte 
        un comportement particulier :
            - si is_cycli est vrai, la valeur est remise à initial_value
            - sinon, une exception est levée
            
        Si cette valeur est None, il n'y a pas de valeur maximum et la 
        croissance de la séquence ira en croissant sans limite.'''
        return self.__maximum_value

    @property
    def is_cyclic(self) -> Optional[bool]:
        '''Indique si la séquence est cyclique.
        
        Une séquence cyclique est une séquence qui possède une valeur maximum 
        et qui, à l'atteinte de cette valeur maximum remet la séquence à la 
        valeur initiale.
            
        Si cette valeur est None, la séquence n'est pas cyclique.'''
        return self.__is_cyclic

    @property
    def prefix(self) -> str:
        '''Le préfixe est la chaîne de caractères mise avant la partie 
        numérique de la séquence lors de la conversion alphanumérique.'''
        return self.__prefix

    @property
    def suffix(self) -> str:
        '''Le suffixe est la chaîne de caractères mise après la partie 
        numérique de la séquence lors de la conversion alphanumérique.'''
        return self.__suffix
    
    @property
    def padding(self) -> tuple[int, str]:
        '''Les informations de remplissage. Un tuple ayant la taille et le 
        caractère de remplissage.'''
        return (self.__padding_size, self.__padding_char)
    
    @property
    def conversion_mode(self) -> tuple[int, str]:
        '''Le mode de conversion de l'entier à la chaîne de caractères.
        
        Un tuple ayant la base et les caractères utilisés pour chaque 
        position de nombre liée à la base.'''
        return (self.__conversion_base, self.__conversion_chars)
    
    @property
    def __len__(self) -> int:
        '''La longueur de la séquence alphanumérique.'''
        return len(self.__current_formatted)
    
    @property
    def __str__(self) -> str:
        '''Représentation sous forme de chaîne de caractères.
        
        La séquence alphanumérique.'''
        return self.__current_formatted
    
    @property
    def current_value(self) -> int:
        '''Retourne la valeur numérique actuelle de la séquence.'''
        if self.__current_value == self.__initial_value - self.__increment_by:
            raise AlphaSequence.ASException('next_value or next_sequence must be called at least once before current_value')
        return self.__current_value
    
    @property
    def current_formatted_value(self) -> str:
        '''Retourne la valeur alphanumérique actuelle de la séquence.'''
        if self.__current_value == self.__initial_value - self.__increment_by:
            raise AlphaSequence.ASException('next_sequence or next_value must be called at least once before current_sequence')
        return self.__current_formatted
    
    @property
    def next_value(self) -> int:
        '''Avance la séquence et retourne sa valeur numérique.'''
        self.__process_next_value()
        return self.__current_value
    
    @property
    def next_formatted_value(self) -> str:
        '''Avance la séquence et retourne sa valeur alphanumérique.'''
        self.__process_next_value()
        return self.__current_formatted


if __name__ == '__main__':
    seq = AlphaSequence(0, 1, prefix='[', suffix=']', padding_size=10, padding_char='_', conversion_chars='0123456789')
    # seq = AlphaSequence(0, 1, prefix='[', suffix=']', padding_size=10, padding_char='_', conversion_chars='0123456789ABCDEF')
    # seq = AlphaSequence(0, 1, prefix='[', suffix=']', padding_size=10, padding_char='_', conversion_chars='01')
    # seq = AlphaSequence(0, 1, prefix='[', suffix=']', padding_size=10, padding_char='_', conversion_chars='▁▂▃▄▅▆▇█')
    
    # nato_alphabet = ('Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliet', 'Kilo', 'Lima', 'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango', 'Uniform', 'Victor', 'Whiskey', 'Xray', 'Yankee', 'Zulu')
    # nato_alphabet = tuple(f'{value}~' for value in nato_alphabet)
    # seq = AlphaSequence(0, 1, prefix='[', suffix=']', padding_size=10, padding_char='_', conversion_chars=nato_alphabet)

    while True:
        print(f'\r{seq.next_formatted_value}', end=' ' * 5)

