
<br />
<p align="center">

  <h3 align="center">PicCollector</h3>

  <p align="center">
    GUI application for scraping and cataloging images from reddit.
    <br />
    <a href="https://github.com/spenat/PicCollector/issues">Report Bug</a>
    ·
    <a href="https://github.com/spenat/PicCollector/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


## About The Project

Collect images from reddit and catalog them with descriptions scraped from the site.
I.e. get all the wallpapers from [Wallpapers](http://reddit.com/r/wallpapers).
Add any subreddit to your list and take home all the pictures.


### Built With

* [Python](https://www.python.org/)
* [tkinter](https://docs.python.org/3/library/tkinter.html)
* [scrapy](https://scrapy.org/)
* [sqlalchemy](https://www.sqlalchemy.org/)
* [pillow](https://python-pillow.org/)
* [falcon](https://falconframework.org/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Install software needed to run PicCollector

* Install Python 3.x with tk/tcl support: [Python](https://www.python.org/downloads/)

* Get pip [pip](https://pip.pypa.io/en/stable/installing/)

* pip
  * Create virtual environment (optional)
  ```sh
  python -m venv temp_env
  source temp_env/bin/activate
  ```

  * Install requirements
  ```sh
  pip install -r requirements.txt
  ```

  * Install requirements for api
  ```sh
  pip install -r requirements_falcon.txt
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/spenat/PicCollector.git
   ```
2. Install python packages
   ```sh
   pip install -r requirements.txt
   ```



## Usage

### Start GUI
```sh
python run.py
```

### Use from commandline (from directory containing the directory PicCollector)
```sh
python PicCollector --help
```

### Create database (optional but recommended)
```sh
python PicCollector --createdb
```

## Roadmap

See the [open issues](https://github.com/spenat/PicCollector/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Project Link: [https://github.com/spenat/PicCollector](https://github.com/spenat/PicCollector)



[contributors-shield]: https://img.shields.io/github/contributors/spenat/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/spenat/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/spenat/repo.svg?style=for-the-badge
[forks-url]: https://github.com/spenat/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/spenat/repo.svg?style=for-the-badge
[stars-url]: https://github.com/spenat/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/spenat/repo.svg?style=for-the-badge
[issues-url]: https://github.com/spenat/repo/issues
[license-shield]: https://img.shields.io/github/license/spenat/repo.svg?style=for-the-badge
[license-url]: https://github.com/spenat/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
