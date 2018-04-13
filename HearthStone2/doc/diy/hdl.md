# HDL - HearthStone Design Language

## Syntax:

1. Basic

```
minion 工程师学徒 {
    id: 7
    rarity: 0
    CAH: 2, 1, 1
    bc: {       # Alias of 'battlecry', set data['battlecry'] = True automatically.
        dc: 1   # Alias of 'draw card'.
    }
    
    `           # Python code
    def func(self):
        pass
    `
}
```
