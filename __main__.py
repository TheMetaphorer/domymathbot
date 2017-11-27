import optparse

print dir()

parser = optparse.OptionParser()
parser.add_option("-s", "-sub", "--subreddit", action=store, type="string", dest="sub")
(options, args) = parser.parse_args()
start(options.sub)