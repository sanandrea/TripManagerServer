// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
// 
//
//  Copyright © 2016 Andi Palo
//  This file is part of project: Simple Loopback Server
//
module.exports = function mountLoopBackExplorer(server) {
  var explorer;
  try {
    explorer = require('loopback-explorer');
  } catch(err) {
    // Print the message only when the app was started via `server.listen()`.
    // Do not print any message when the project is used as a component.
    server.once('started', function(baseUrl) {
      console.log(
        'Run `npm install loopback-explorer` to enable the LoopBack explorer'
      );
    });
    return;
  }

  var restApiRoot = server.get('restApiRoot');

  var explorerApp = explorer(server, { basePath: restApiRoot });
  server.use('/explorer', explorerApp);
  server.once('started', function() {
    var baseUrl = server.get('url').replace(/\/$/, '');
    // express 4.x (loopback 2.x) uses `mountpath`
    // express 3.x (loopback 1.x) uses `route`
    var explorerPath = explorerApp.mountpath || explorerApp.route;
    console.log('Browse your REST API at %s%s', baseUrl, explorerPath);
  });
};
