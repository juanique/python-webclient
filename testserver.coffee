fs = require("fs")

app = require("express").createServer()
app.use require("connect").bodyParser()

app.get "/$", (req, res) ->
  res.send("this is text")

app.get "/data.json$", (req, res) ->
  res.json(name : "coca cola")

app.get "/echo_get$", (req, res) ->
  res.json(req.query)

app.post "/echo_post_json$", (req, res) ->
  res.json(req.body)

app.post "/echo_post_multipart$", (req, res) ->
  console.log(req.body)
  res.json(req.body)

app.post "/echo_post_files$", (req, res) ->
  response = {
    param1: req.body.param1,
    param2: req.body.param2,
  }
  fs.readFile req.files.textfile.path, (err, data) =>
    response.textfile = data.toString()
    console.log response
    res.json(response)

app.get "/test_auth", (req, res) ->
  encodedCredentials = req.headers['authorization'].split("Basic ").pop()
  decodedCredentials = new Buffer(encodedCredentials, "base64").toString("ascii")
  [username, password] = decodedCredentials.split(":")

  res.json( username : username, password : password)

app.listen(3000)
