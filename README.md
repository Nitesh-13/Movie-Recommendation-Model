# Movie Recommender

Movie Recommender Model is a program which uses scikit-learn library to find smilar movies from the movies dataset and return it to the user.
This repo has 2 versions i.e. A Console Version and A Web Interface Version which uses flask server.

## Installation

1. Clone this repository:

```shell
git clone https://github.com/Nitesh-13/Movie-Recommendation-Model.git
```

2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the required modules listed in [requirements.txt](https://github.com/Nitesh-13/Movie-Recommendation-Model/blob/main/requirements.txt).

```bash
pip install -r /path/to/requirements.txt
```

3. Now run the python program. If you are running the web app , after executing the script, visit "[127.0.0.1](http://127.0.0.1:5000/)" to view the program.
4. When modifying, the directory structure is as follows

   ```python
   Movie-Recommendation-Model/
   ├── static/
   │   ├── css/
   │   │   └── style.css /*Css Styles*/
   │   ├── js/
   │   │   └── script.js /*Js Script*/
   │   ├── img/
   │   │   └── image.png /*If Any present*/
   │   └── favicon.ico
   ├── templates/
   │   └── index.html
   ├── web_app.py
   ├── movie_dataset.csv
   ├── .gitignore
   └── requirements.txt
   ```

## Contributing

We welcome and greatly appreciate any and all pull requests from the community, as they help to improve and enhance the quality of our project.

## License

[MIT](https://choosealicense.com/licenses/mit/)
