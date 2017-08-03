for /l %%x in (1, 1, 900) do (
   start cmd.exe @cmd /k "python -m tests.stress_tests.simulator Rooom %%x &"
   TIMEOUT 1
)