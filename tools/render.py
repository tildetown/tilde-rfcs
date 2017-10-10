"""Python script to convert TildeRFC documents (text,markdown) into HTML."""

import markdown,re,argparse
from mdx_gfm import GithubFlavoredMarkdownExtension

RFC_NUM_TEXT_FORMAT = re.compile("^RFC (\d+)")
OUTPUT_DIR = "/home/minerobber/public_html/tilderfcs/"

def get_document(filename,format):
	with open(filename) as f:
		# TODO: make this a modular system, would make adding new formats easier
		if format=="text":
			lines = [line.strip() for line in f.readlines()]
			title = lines.pop(0)
			rfcnum = RFC_NUM_TEXT_FORMAT.match(title).group(1)
			ret = dict(title=title,number=int(rfcnum),author=lines.pop(0),status=" ".join(lines.pop(0).split()[1:])) # Required data
			# Optional fields
			if lines[0].startswith("Updates: "):
				ret["updates"]=[int(p) for p in lines.pop(0)[8:].split(", ")]
			if lines[0].startswith("Updated by: "):
				ret["updated-by"]=[int(p) for p in lines.pop(0)[11:].split(", ")]
			if lines[0].startswith("Errata Exist"):
				ret["errata"]=True
				lines.pop(0)
			ret["errata"] = ret.get("errata",False)
			ret["rendered"]="<p>"+"\n".join(lines).replace("\n\n","</p><p>")
			ret["format"]="TXT"
			ret["link"]="https://github.com/tildetown/tilde-rfcs/blob/master/"+filename
			return ret
		elif format=="markdown":
			lines = [line.strip() for line in f.readlines()]
			title = lines.pop(0)[2:]
			rfcnum = RFC_NUM_TEXT_FORMAT.match(title).group(1)
			ret = dict(title=title,number=int(rfcnum))
			while not lines[0].startswith("|Author|"):
				lines.pop(0)
			ret["author"] = lines.pop(0)[8:-1]
			ret["status"] = lines.pop(0)[9:-1]
			if lines[0].startswith("|Updates|"):
				ret["updates"] = [int(p) for p in lines.pop(0)[10:-1].split(", ")]
			if lines[0].startswith("|Updated by|"):
				ret["updated_by"] = [int(p) for p in lines.pop(0)[13:-1].split(", ")]
			if lines[0]=="|Notices|Errata Exist|":
				ret["errata"] = True
				lines.pop(0)
			ret["errata"] = ret.get("errata",False)
			ret["rendered"] = markdown.markdown("\n".join(lines),extensions=[GithubFlavoredMarkdownExtension()])
			ret["format"] = "MD"
			ret["link"]="https://github.com/tildetown/tilde-rfcs/blob/master/"+filename
			return ret
		else:
			raise TypeError("Invalid format")

html_header = """<html>
<head>
<title>{title}</title>
<style>
</style>
</head>
<body>
<h1>{title}</h1>
<h2>by {author}</h2>
<table><tr><td>[<a href="../index.html">Index</a>]</td><td>[<a href="{link}">{format}</a></td></tr></table>"""

def to_html(loadedrfc):
	output = html_header.format(**loadedrfc)
	if loadedrfc.get("updates"):
		output += "<h3>Updates: "+", ".join(["<a href='{0}.html'>{0}</a>".format(str(p)) for p in loadedrfc["updates"]])+"</h3>"
	if loadedrfc.get("updatedby"):
		output += "<h3>Updated by: "+", ".join(["<a href='{0}.html'>{0}</a>".format(str(p)) for p in loadedrfc["updatedby"]])+"</h3>"
	if loadedrfc["errata"]:
		output += "<h4 style='color:red;'>Errata Exist</h4>"
	output += loadedrfc["rendered"]
	output += "\n</body>\n</html>"
	with open(OUTPUT_DIR+str(loadedrfc["number"])+".html","w") as f:
		f.write(output)

INVALID_STATES = ((True,True),(False,False),(None,None))

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="A program to render RFCs to an output directory.")
	parser.add_argument("input",help="The file to render.")
	parser.add_argument("--text","-t",action="store_true",help="Render input as text.")
	parser.add_argument("--markdown","-m",action="store_true",help="Render input as markdown.")
	args = parser.parse_args()
	if (args.text,args.markdown) in INVALID_STATES:
		raise Exception("--text or --markdown (one or the other) must be supplied.")
	if args.text:
		to_html(get_document(args.input,"text"))
	elif args.markdown:
		to_html(get_document(args.input,"markdown"))
