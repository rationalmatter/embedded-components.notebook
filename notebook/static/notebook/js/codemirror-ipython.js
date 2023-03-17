// IPython mode is just a slightly altered Python Mode with `?` beeing a extra
// single operator. Here we define `ipython` mode in the require `python`
// callback to auto-load python mode, which is more likely not the best things
// to do, but at least the simple one for now.

(function(mod) {
  if (typeof exports == "object" && typeof module == "object"){ // CommonJS
    mod(requirejs("codemirror/lib/codemirror"),
        requirejs("codemirror/mode/python/python")
        );
  } else if (typeof define == "function" && define.amd){ // AMD
    define(["codemirror/lib/codemirror",
            "codemirror/mode/python/python"], mod);
  } else {// Plain browser env
    mod(CodeMirror);
  }
})(function(CodeMirror) {
    "use strict";

    CodeMirror.defineMode("ipython", function(conf, parserConf) {
        var pythonConf = {};
        for (var prop in parserConf) {
            if (parserConf.hasOwnProperty(prop)) {
                pythonConf[prop] = parserConf[prop];
            }
        }
        pythonConf.name = 'python';
        pythonConf.singleOperators = new RegExp("^[\\+\\-\\*/%&|@\\^~<>!\\?]");
        if (pythonConf.version === 3) {
            pythonConf.identifiers = new RegExp("^[_A-Za-z\u00A1-\uFFFF][_A-Za-z0-9\u00A1-\uFFFF]*");
        } else if (pythonConf.version === 2) {
            pythonConf.identifiers = new RegExp("^[_A-Za-z][_A-Za-z0-9]*");
        }
        // Jupyter extends Python mode with additional configuration; we
        // extend Jupyter's ipython mode by making sure there is no 
        // non-styled text in the CodeMirror editor, i.e. that all text
        // is in some <span> element. We do this by overriding ipython
        // mode's token function, returning dummy style when ipython 
        // detects none. This is needed due to a WebKit bug in iOS, which
        // renders caret funny in some cases.
        var ipythonMode = CodeMirror.getMode(conf, pythonConf);
        return {
            startState: function(basecolumn) {
                return ipythonMode.startState(basecolumn);
            },
            token: function(stream, state) {
                var superToken = ipythonMode.token(stream, state);
                return superToken ? superToken : "notoken";
            },
            indent: function(state, textAfter) {
                return ipythonMode.indent(state, textAfter);
            },
            electricInput: ipythonMode.electricInput,
            closeBrackets: ipythonMode.closeBrackets,
            lineComment: ipythonMode.lineComment,
            fold: ipythonMode.fold
        };
    }, 'python');

    CodeMirror.defineMIME("text/x-ipython", "ipython");
})
