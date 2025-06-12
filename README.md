# GitPeek
A simple CLI tool to fetch and display recent Github user activity using the GitHub API

## Features

- Fetches recent public activity of a GitHub user.
- Displays activity in a clean, readable format.
- Simple and easy to use CLI.
- Written in Python with no external libraries for fetching data.

## Installation

1.  Clone the repository:
    ```sh
    git clone https://github.com/aleng1/GitPeek.git
    ```
2.  Navigate to the project directory:
    ```sh
    cd GitPeek
    ```
3.  Install the package using pip:
    ```sh
    pip install .
    ```

## Usage

To fetch a user's GitHub activity, run the following command:

```sh
gitpeek <username>
```

Replace `<username>` with the GitHub username of the person whose activity you want to see.

### Example

```sh
gitpeek torvalds
```

## Output Example

```
$ gitpeek torvalds
Fetching activity for torvalds...
Found 30 recent events for torvalds:
- Pushed 1 commit to torvalds/linux-roadmap
- Opened pull request #8775 in torvalds/linux-roadmap
- Pushed 9 commits to torvalds/linux-roadmap
...
```

## Supported Events

GitPeek currently parses and displays the following GitHub events:

- `PushEvent`: Commits pushed to a repository.
- `IssuesEvent`: A new issue is opened.
- `IssueCommentEvent`: A comment is made on an issue.
- `WatchEvent`: A repository is starred.
- `PullRequestEvent`: A pull request is opened.
- `CreateEvent`: A repository, branch, or tag is created.
- `DeleteEvent`: A branch or tag is deleted.
- `ForkEvent`: A repository is forked.
- `PublicEvent`: A private repository is made public.

## Development

This project uses Python's standard library to make API requests.

The main API endpoint used is: `https://api.github.com/users/<username>/events`

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions for improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
