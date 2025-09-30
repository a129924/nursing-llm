from typing import TypeVar

# Define Schema and Entity type variables for generic use
Schema = TypeVar("Schema")
Entity = TypeVar("Entity")

# Define T as a covariant type variable
T = TypeVar("T", covariant=True)
