# MAKE ĆWIKI GREAT AGAIN 

## Usage:

Input template:  
```json
{  
 "points": {
        "000001": "1",  
        "000002": "2"  
    },  
    "declarations": {  
        "000001": ["1", "2", "3"],  
        "000002": ["1", "2", "4"]  
    },  
    "priority": {  
        "000001": "1"  
    }  
}
```

Run with: `python3 main.py -input="name_of_your_file.json"`  
You can also add a custom `-expect_out=true` flag, which will generate a new JSON containing points calculated after initial queue was satisfied.  

Example output:
```
Zadanie 1a: @000001  
Zadanie 1b: @000002  
Zadanie 2:  @000002  
Zadanie 3:  @000001  
Zadanie 4:  @000002  
```