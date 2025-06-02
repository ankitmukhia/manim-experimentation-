```shell
uv run -- python -m manim main.py MyScene -pql
```
 
Will create media folder where your generated file exists as mp4. And if you are on linux there may be problem with auto open command tool. But that doesn't block your generate/render. It will error at last after mp4 has generated. or you can avoid the command from ```bash -pql ``` to ```shell --ql ```.
