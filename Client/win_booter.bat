for /l %%x in (1, 1, 5) do (
   start cmd.exe @cmd /k "python -m tests.stress_tests.simulator Rooom %%x &"
)