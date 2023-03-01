# Error recovery 

##### During the project: 

- explored different error recovery strategies during parsing,
- implemented different error recovery strategies,
- many examples are given that demonstrate the differences in error recovery strategies, emphasizing their advantages and disadvantages.

## 1. Launch

##### Launching the Phase Level Recovery strategy

Parser: `python ./parser_phase_level.py <path to the file to be analyzed> <path to the directory where the temporary file can be stored>`

All errors will be recorded in the file.out file, which will be created next to the analyzed file.

##### Launching the Phase Level Recovery strategy

Parser: `python ./parser_panic_mode.py <path to the file to be analyzed> <path to the directory where the temporary file can be stored>`

## 2. Tasks

##### Tatiana Elfimova

- Lexer and parser for a specific language written using `ply.lex` and `ply.yacc`
- Implementation of one strategy
- Tests
- Comparison of two implementations


##### Alexander Mosin

- Research on different strategies
- Writing a parser for one strategy
- Examples
- Comparison of two implementations

## 3. Language Syntax

The grammars follow these rules:

- The start symbol is enclosed in `< >`
- Non-terminals are enclosed in `' '`
- Terminals are enclosed in `" "`
- Empty string is represented by `e`
- Rule:
  - `non-terminal = (terminals and non-terminals) ,`
  - Each rule should be written on a single line
  - There should be no empty rules
  
  
Example of a correct grammar: 

```
<E> = e,
`E` = "["`E`"]",
`E` = `E``E`,
```

## 4. Description of the selected strategies

#### Phase Level Recovery

Phase Level Recovery straragy was used ([link](https://www.geeksforgeeks.org/error-recovery-strategies-in-compiler-design/)). In this strategy, errors are corrected as they are found: one line is processed, and if an error is found in it, the error is corrected. The analysis does not move to a new line until the current line is fully correct (for example, in the example below, the first line is corrected by replacing two tokens with one non-terminal, followed by inserting a comma).

###### Example of the process:

###### Test:

```
<E> `A` = e
`E` = "(" `E` ")"

`E` = e
`E` "a"
```

###### Output:

```
You should use one non_terminal before arrow :1
Expected `,` :1
Expected `,` :2
Expected rule :3
Expected `,` :4
Expected rule :5
```

##### Advantages of the strategy:

- Can be easily applied to different grammars
- It is possible to find many different errors in one line

##### Disadvantages of the strategy:

-The need to analyze and process each specific error, as well as think through how to correct it.
  

##### More information about other strategies is available in the file (in Russian): [Исследование_различных_стратегий.pdf](https://github.com/tanya011/fl-2022-hse-win/blob/proj/%D0%98%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D1%80%D0%B0%D0%B7%D0%BB%D0%B8%D1%87%D0%BD%D1%8B%D1%85_%D1%81%D1%82%D1%80%D0%B0%D1%82%D0%B5%D0%B3%D0%B8%D0%B9.pdf)

## 5. Comparison of two strategies

Let's see how the strategies work on different examples:

#### Example 1: Error - extra token

```
`E` = "(" ")" , "(" ")",
```

##### Output (Phase mode recovery):

```
You shouldn't use commas between tokens :1
```

###### Explanation:

Such an error was predicted and handled.

##### Output (Panic mode recovery):

```
All characters after the ending character (,) have been deleted
```

###### Explanation:

As we can see, the Panic Mode implementation simply discards all symbols after the ‘,’ - in this case *"(" ")".*. Therefore, only the first part of the input string is left.

```
`E` = "(" ")" ,
```

The string `*"(" ")"*` is a correct string and there was no need to discard it, it was enough to simply remove the extra comma.

###### Conclusion: The phase mode recovery worked better on this example.

#### Example 2: Error - not have END

```
`E` = "(" ")"
```

##### Output (Panic mode recovery):

```
You have to add an end of line character (,)
```

##### Output (Phase mode recovery):

```
Expected `,` :1
```

###### As we can see, both implementations suggest adding an end-of-line character to the input string. In this example, both strategies will work the same way.

#### Example 3: Error - not have non-terminal

```
“a” = “b”,
```

##### Output (Panic mode recovery):

```
This rule has been removed because it does not contain non-terminal characters
```

###### Explanation:

Since there is no non-terminal symbol at the beginning of the string, the panic mode method will see an error right at the beginning and will therefore remove all symbols that come after it. As a result, it will remove the entire string, which means that the rule will be deleted.

##### Output (Phase mode recovery):

```
You should use one non_terminal before arrow :1
```

###### It appears that on this example, both strategies will work the same way.

#### Example 4: 

```
`E` = "(" ")" ,,,,,,
```

##### Output (Panic mode recovery):

```
All characters after the first ending character (,) have been deleted
```

###### Explanation:

In panic mode, all symbols after the first comma will be discarded, regardless of what follows.

##### Output (Phase mode recovery):

```
Unexpected END(,) :1
```

###### Explanation:

The parser does not expect to receive such a string because the corresponding case is not handled. We have not specified what to do in this situation and how to transform such a string into a correct one in order to continue its processing and search for other errors.

###### In this example, we can conclude that the Panic mode will work better.



## 5. Conclusion:

##### Main advantages of Panic mode over Phase mode

- simpler implementation
- handles any error
- never terminates with an error

##### Main advantages of Phase mode over Panic mode

- can handle more than one error in a single string
