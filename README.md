# novelyst_timeline

A *Timeline* converter plugin for novelyst.

For more information, see the [project homepage](https://peter88213.github.io/novelyst_timeline) with description and download instructions.

## Development

*novelyst_timeline* depends on the [pywriter](https://github.com/peter88213/PyWriter) and [yw-timeline](https://github.com/peter88213/yw-timeline) libraries which must be present in your file system. It is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

### Mandatory directory structure for building the application script

```
.
├── PyWriter/
│   └── src/
│       └── pywriter/
├── yw-timeline/
│   └── src/
│      └── ywtimelinelib/
└── novelyst_timeline/
    ├── src/
    ├── test/
    └── tools/ 
        └── build.xml
```

### Conventions

- Minimum Python version is 3.6. 
- The Python **source code formatting** follows widely the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide, except the maximum line length, which is 120 characters here.

### Development tools

- [Python](https://python.org) version 3.9
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and [EGit](https://www.eclipse.org/egit/)
- [Apache Ant](https://ant.apache.org/) for building the application script


## License

novelyst_timeline is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
