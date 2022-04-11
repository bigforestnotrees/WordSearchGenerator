# WELCOME!

To use the word search generator, simply modify the word_list variable in the file and use the following command:

    $ python wordsearchgen.py

Default output, with word_list = ["Hello", "World"] and size = 25:

    C U U R J Q G L Q F K A X M X X Y F E K J V T F A
    Y A X R Q E G T V I T E T M I Y K V O N N Y R V P
    F T X L L F D G M I M N Q W Q O Y L K H T P I J E
    W W R U M X X V K O K B Z B R O Q S D L Q V P T Z
    H O O I K Y A M W M F K H Q V J D T I Y E E R V A
    L L L R H Z W Z V U L L S R P W J D T V I I M N S
    X U H L L X V P Q J T L U D G Y W N J E M U W B N
    X S G B E D I X I S O P A Z D C V W L Q H P Q H Y
    U G J M R H E Z C J O E E R E G O N S U T G X G G
    L H P M Q T T R C M N C E E Z X D L I J G G D X K
    D S P U U A Q C O R Z W J O I Z G D Z I A C A Y K
    B L E W S Z E N R D W E L U J D J I W A N I L K P
    C H U Q O V E T D S Z U F E V P E T F H F M U A J
    X W I C A H X T C T R N Z Z Y I G B G I S D O N I
    N U D V S N Z M N R N C P O H D N D V Y A M B F L
    O K S E C G T A L Q A Y U R N N O Z F Q H K S G U
    J Q Z T N K C O B W R T L S T K O C H Q P A O V Q
    F P K J S Q C M P L T F Z S C A V W G P K V P M M
    F C U P H V R T J N B W Z I Y A U Q X B C Z T B X
    O C T T M O O P C M Y T I D D L W T F U Z E S I L
    A T Q G X J X S T T I F N U Z G O Q O K T X D P A
    F H D E B J Y R P X H Y C B O V K X E W G R H Y Y
    W Z O T C S I P T B A Q X E H Z E T J O C L S G P
    C C N B Q I E B K A N H O T E N Z H B K S Q G G U
    Z I W M W I A Q J D X A M X H F W B L M S P L Y L

To generate different results on the same input, pass seeded=True to the constructor, like so:

    x = SquareWordSearch(word_list, size=25, seeded=True)

Enjoy!