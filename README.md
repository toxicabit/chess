# Техническое задание проекта "Шахматная программа".

## Цель проекта.
**Целью проекта** является написание программы, способной играть в шахматы на приемлемом уровне. 
Под *приемлемым уровнем* подразумевается высокая вероятность выигрыша у игроков с низким и 
среднем уровнем игры в шахматы. 

## Задача.
Программа будет представлять собой некоторое вычислительное ядро(движок) осуществляющее все 
рассчёты, связанные с выигрышной стратегией и тактикой. Ядро будет снабжено возможностью ввода
и вывода данных и "обёрнуто" в графическую  оболочку, чтобы пользователь имел возможность 
осуществлять ход, и непосредственно выдеть ходы компьютера. 

## Основные подзадачи.

Обозначенные цель и задача формируют следующий ряд подзадач, реализация которых необходима для
успешного воплощения в жизнь проекта:

>1. Реализация представления доски.
>2. Реализация вычислительного ядра. 
>3. Реализация возможностей ввода/вывода информации.
>4. Реализация графической оболочки. 
>5. Тестирование программы, устранение багов.

Также, при успешном выполнении поставленных подзадач, ставится дополнительная подзадача:

>1. Оптимизация вычислительного ядра.

## Описание подзадач.

### 1. Реализация представления доски.

В связи с особенностями Python доска будет реализована на основе bitset'ов. Для каждого типа фигур
будет реализован свой bitboard, т.е. 64-битный набор, такой, что ноль соответствует осутствию фигуры
данного типа в позиции, а единица - присутствию. Также реализуются дополнительные битборды для 
вычисления возможного хода и прочих внутриигровых целей. 

### 2. Реализация вычислительного движка. 

Для успешной реализации вычислительного движка, помимо представления доски, понадобятся три обязательные 
функции: функция вычисления состояний доски, которые могут быть достигнуты из текущего состояния, 
эвристическая функция оценки хода, функция Альфа-Бета редукции, позволяющая рассматривать самые ценные
ветки дерева состояния, и совершать компьютеру наиболее выгодные ходы. 

### 3. Реализация возможностей ввода вывода. 

Реализация функции передачи вычислительному ядру желаемого пользователем хода. После чего ядро должно оценить,
удовлетворяет ли желаемый ход правилам игры, если да, то через функции вывода сообщить игроку об изменении 
текущего состояния доски, иначе ждать корректного хода. На вход функции будет подаваться текущая позиция 
и желаемая позиция. 

### 4. Реализация графической оболочки.

Реализация графического представления доски и фигур, реализация канал обмена информацией между пользователем
и ядром посредством удобной визуализации. Вся графическая оболочка будет реализована посредством использования
средств библиотеке PyGame. 

### 5. Тестирование программы. 

Тестирование отдельных модулей, отдельных функций, программы в целом. 

## Используемые средства.

Используемые средства:

>1. Операционная система Windows 10
>2. Google Colaboratory
>3. PyCharm 2020.2.3 x64
>4. Python 3.9
>5. Библиотека bitarray
>6. Библиотека PyGame
