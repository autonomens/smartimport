<!doctype html>

<HTML lang="fr">
  <HEAD>
    <title>Smart Import</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" 
    href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" 
    integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" 
    crossorigin="anonymous"
    >
    <link rel="stylesheet" type="text/css" href="/static/smart-import.css">
  </HEAD>

  <body>
    <div id="home">
      <h1>Smart Import</h1>
      % if json:
        <form action="/?json=True" method="POST" enctype="multipart/form-data">
      % end
      % if not json:
        <form action="/" method="POST" enctype="multipart/form-data">
      % end
        <h3> 1 - Select a file </h3>
        <input name="data_file" type="file" />
        <h3> 2 - Launch Smart Import </h3>
        <input value="GO" type="submit" />
      </form>
    </div>
  </body>
</html>

