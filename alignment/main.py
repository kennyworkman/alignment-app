"""

main
~~~~
Intened as entrypoint for package build.

"""


from alignment import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
