<!doctype html>
<!-- page.tpl -->
<HTML lang="fr">
  <HEAD>
     <TITLE>Smart Import</TITLE>
     <meta charset="UTF-8">
     <link rel="stylesheet" type="text/css" href="/static/smart-import.css">
  </HEAD>

  <body>
    <h1>Smart Import</h1>
    <form action="/smartimport" method="POST" enctype="multipart/form-data">
      <h3> 1 - Select a file </h3>
      <input name="data_file" type="file" />
      <h3> 2 - Launch Smart Import </h3>
      <input value="GO" type="submit" />
    </form>
  </body>
</html>

