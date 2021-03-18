# Just snip

A simple tool to manage your snippets.  Something like git or docker, only for snippets.

## Motivation

How do I make my snippets available on work laptop?  I've sent via email...  
How do I keep two copies in-sync then?  Well, I do not, but I might've gone through the process each time I update one of them  
How do I modify the existing snippet?  Paste - modify - "snippetize" - replace?  Seems like too laborious, hinders improvement, not tracked by any VCS  
How do I see my snippets?  A bit easier if they are one-liners - just open python.json or whatever  
How do I group my snippets?  You don't

## Trace

cd ~/.config/Code/User/snippets  
-> git init && git add . && git commit -m "Init"

## Usage

Smth along the lines of

```bash
snip init
```

```bash
snip push
    # Transitioned to snip init
    # # [PATH LIKE ~/.config/Code/User/snippets/]
    # # [URL LIKE https://github.com/ihor-durnopianov/snippets]
```

```bash
snip pull
    # Transitioned to snip init
    # # [URL LIKE https://github.com/ihor-durnopianov/snippets]
    # # [PATH LIKE ~/.config/Code/User/snippets/]
```

```bash
snip add
    lang
    prefix [required if not review else optional]
    [--review]
    [--edit-msg]
```
-> editor for snippet pops up  
-> Save  
-> (if review) editor with snippet itself pops up (s.t. one can set prefix and description)  
-> Save  
-> (if edit-msg) editor with (pre-filled) commit message pops up  
-> Save

```bash
snip edit
    [lang]
    prefix
    [--edit-msg]
```
-> editor for snippet pops up  
-> Save  
-> editor with snippet itself pops up (s.t. one can set prefix and description)  
-> Save  
-> (if edit-msg) editor with (pre-filled) commit message pops up  
-> Save

```bash
snip list
    [lang]
    [tag0 tag1 ...]
```

```bash
snip status?
```

