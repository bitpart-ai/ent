# Ent, the talking tree

Welcome to Bitpart's coding assignment. In this repository, you'll find scaffolding for a small Python library called `ent` along with a test suite. The library models a simple version of a hierarchical task network (HTN) domain. 

<details>

<summary>What is an HTN? What is a domain?</summary>

HTN is a model used for planning. An HTN is described by its domain, which consists of tasks, task methods, and actions. Tasks are hierarchical and are decomposed by a planning procedure in order to produce a series of actions that form a plan. Task methods are different ways to perform a task. As an example, we may have a task `have breakfast`, which has three methods. The first method is a sequence `[go to diner, order pancakes, eat]`, the second is `[go to kitchen, make pancakes, eat]`, and the third is `[go to kitchen, make coffee, drink]`. An element in a task method can be either an action or a task (the latter gives the HTN its hierarchical nature).

For more background on HTN planning, see [this Game AI Pro article](https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter12_Exploring_HTN_Planners_through_Example.pdf).

</details>

## Understanding the test data

In this assignment, you'll be asked to construct an HTN domain from a [data file](tests/fixtures/transcript.csv), which we call a transcript.

Here is a snippet of the transcript.

|type   |character|verb                         |details                                                                                                          |task                         |method instance|
|-------|---------|-----------------------------|-----------------------------------------------------------------------------------------------------------------|-----------------------------|---------------|
|SUBTASK|         |read_novel                   |                                                                                                                 |pass_time_at_baker_st        |1              |
|STEP   |WATSON   |PICKS_UP                     |{"object": "novel"}                                                                                              |read_novel                   |2              |
|STEP   |WATSON   |SITS_DOWN                    |{"target": "armchair"}                                                                                           |read_novel                   |2              |
|STEP   |WATSON   |SPEAKS_TO                    |{"target": "HOLMES", "utterance": "It's far too hot out today to do anything but stay indoors."}                 |read_novel                   |2              |
|SUBTASK|         |smoke_pipe                   |                                                                                                                 |pass_time_at_baker_st        |3              |
|STEP   |HOLMES   |PICKS_UP                     |{"object": "tobacco"}                                                                                            |smoke_pipe                   |4              |
|STEP   |HOLMES   |PLACES_IN                    |{"object": "tobacco", "target": "pipe"}                                                                          |smoke_pipe                   |4              |
|STEP   |HOLMES   |SMOKES                       |{"object": "pipe"}                                                                                               |smoke_pipe                   |4              |
|STEP   |WATSON   |SPEAKS_TO                    |{"target": "HOLMES", "utterance": "Where ever did you get that slipper in which you keep your tobacco, Holmes?"} |smoke_pipe                   |4              |
|STEP   |HOLMES   |SPEAKS_TO                    |{"target": "WATSON", "utterance": "That is too long a story for a day as hot as today, Doctor."}                 |smoke_pipe                   |4              |

The transcript describes sequences of behavior and is annotated with how they should be structured when turned into an HTN domain. Every row in the transcript represents either a `subtask` or `step`, indicated in the `type` column. `step` rows describe actions - primitive and concrete steps taken by a character. For example, the second row in the transcript describe a "PICKS_UP" action (`verb` column) performed by the character "WATSON" (`character` column) in which Watson picks up a "novel" object (`details` column). For the purposes of the assignment, we won't have to worry about where verbs are defined and what is a valid binding of the variables in an action's details - we'll assume whatever's in the transcript is valid.

`step` rows are annotated with the task they are a child of (`task` column) and the instance id for the task method described by that annotation (`method instance` column). Consider the second through fourth lines in the transcript (the three consecutive `step` rows). Taken together, they describe a task method for the task `read_novel`, which has three children: a PICKS_UP action, a SITS_DOWN action, and a SPEAKS_TO action.

`subtask` rows describe explicit domain structure. That is, rather than specifying concrete actions, they describe parent-child relationships between task methods and tasks. The first row below is stating that there is a task method for the task `pass_time_at_baker_st` which has one child, `read_novel`, which is itself a task. The fifth row is stating that there is a task method for the task `pass_time_at_baker_st` that has a single child, `smoke_pipe`.

Note that a single method instance can have many subtask children - we could have a task method for `pass_time_at_baker_st` with three consecutive task children, e.g., `[read_novel, smoke_pipe, take_a_nap]`.

## Problem 1: Build a domain

The first problem is to construct a domain using the transcript file. All of the requisite types are provided in the library code (`Domain`, `Task`, `TaskMethod`, and `Action`). The function stub to be filled out is `Domain.from_transcript_rows`. See `tests/test_domain.py` for how the method is expected to be called.

For the transcript snippet above, the domain produced would be structured like

```
(Task pass_time_at_baker_str
  (TaskMethod
    [read_novel])
  (TaskMethod
    [smoke_pipe]))

(Task read_novel
  (TaskMethod
    [(Action WATSON PICKS_UP novel)
     (Action WATSON SITS_DOWN armchair)
     (Action WATSON SPEAKS_TO HOLMES "It's far too hot...")]))

(Task smoke_pipe
  (TaskMethod
    [(Action HOLMES PICKS_UP tobacco)
     (Action HOLMES PLACES_IN tobacco pipe)
     (Action HOLMES SMOKES pipe)
     (Action WATSON SPEAKS_TO HOLMES "Where ever did you get...")
     (Action HOLMES SPEAKS_TO WATSON "That is too long a story...")]))
```

This is just a notation for showing the structure of a domain, not anything to do with the actual expected output.

For both problems, you are free to change any code you like, although the tests should pass without being modified.

## Problem 2: Generate dialogue choices

Once you've got a domain constructed from the data in the test transcript, the next problem is to generate dialogue choices using the domain. The function stub to be filled out is `Domain.get_dialogue_choices`. See `tests/test_domain.py` for how the method is expected to be called.

Using the small domain from the snippet above, we can walk through an example call of this method:

```python
observed_sequence = [
    Action("WATSON", "PICKS_UP", {"object": "novel"}),
    Action("WATSON", "SITS_DOWN", {"object": "armchair"}),
]
domain.get_dialogue_choices("read_novel", observed_sequence)

>>> [Action("WATSON", "SPEAKS_TO", {"target": "HOLMES", "utterance": "It's far too hot..."})]
```

Dialogue choices are generated by finding every valid next "SPEAKS_TO" action given an observed history of actions. In the above example, the observed history is a prefix of the one task method for `read_novel` in our small domain. Since the action that immediately follows that prefix is a "SPEAKS_TO" action, we select it as a valid dialogue choice.

Consider a more complex example. For a domain

```
(Task read_novel_with_reaction
  (TaskMethod
    [(Action WATSON PICKS_UP novel)
     (Action WATSON SITS_DOWN armchair)
     (Task comment_on_novel)]))

(Task comment_on_novel
  (TaskMethod
    [(Action HOLMES SPEAKS_TO WATSON "I love that book.")])
  (TaskMethod
    [(Action HOLMES SPEAKS_TO WATSON "That book stinks.")]))
```

Now our same example method call from before results in

```python
observed_sequence = [
    Action("WATSON", "PICKS_UP", {"object": "novel"}),
    Action("WATSON", "SITS_DOWN", {"object": "armchair"}),
]
domain.get_dialogue_choices("read_novel_with_reaction", observed_sequence)

>>> [
        Action("HOLMES", "SPEAKS_TO", {"target": "WATSON", "utterance": "I love that book."}),
        Action("HOLMES", "SPEAKS_TO", {"target": "WATSON", "utterance": "That book stinks."}),
    ]
```

In order to get all of the valid dialogue choices, we had to expand the `comment_on_novel` task which was the next step in the task method we matched the observed sequence against. Each method for `comment_on_novel` starts with a "SPEAKS_TO" action, so we can select each of the actions as a valid choice.

## Running the tests

Create a virtual environment (named `env` here):

```
python -m venv env
```

Activate virtual environment:

```
source env/bin/activate
```

Install the package as editable:

```
pip install -e ".[dev]"
```

Run tests (must be run from the root of the repo):

```
pytest
```
