Uptrack is a web application to track how up to date your downstream
distribution is compared to the upstream distros you are based on.

It is useful if you rebuild a distribution from source, eventually adding
packages or modifying some of them, but that you want to make sure you do not
lag behind.

Development happens [on Github](https://github.com/network-box/uptrack), no
stable releases have been made yet.

## Getting Started

To get started with a development instance of Uptrack, run the following
commands:

```
$ git clone git://gitorious.org/bochecha-dayjob/uptrack.git
$ cd uptrack
$ virtualenv --system-site-packages venv
$ . ./venv/bin/activate
$ python setup.py develop
$ initialize_uptrack_db development.ini
$ pserve development.ini
```

An account is created by default, so you can sign in:
* Login: `admin`
* Password: `admin`

More details can be found in
[the documentation](http://bochecha.fedorapeople.org/uptrack-docs/).

## Legal

Uptrack was started for our needs at [Network Box](https://www.network-box.com/),
but we want it to be generally reusable for others, which is why we decided to
publish it under the
[GNU Affero General Public License](http://www.gnu.org/licenses/agpl.html),
either version 3 or any later version.

We won't ask you to sign a copyright assignment or any other long and tedious
legal document, so just send us patches and/or pull requests!
