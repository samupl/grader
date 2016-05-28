(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var defaultToWhiteSpace, escapeRegExp, ltrim, makeString, parseFile, parseFileFallback, trimLeft;

module.exports = function(input) {
  var add, chunk, current, del, deleted_file, file, files, from_file, index, j, len, line, lines, ln_add, ln_del, new_file, noeol, normal, parse, restart, schema, start, to_file;
  if (!input) {
    return [];
  }
  if (input.match(/^\s+$/)) {
    return [];
  }
  lines = input.split('\n');
  if (lines.length === 0) {
    return [];
  }
  files = [];
  file = null;
  ln_del = 0;
  ln_add = 0;
  current = null;
  start = function(line) {
    var fileNames;
    file = {
      chunks: [],
      deletions: 0,
      additions: 0
    };
    files.push(file);
    if (!file.to && !file.from) {
      fileNames = parseFile(line);
      if (fileNames) {
        file.from = fileNames[0];
        return file.to = fileNames[1];
      }
    }
  };
  restart = function() {
    if (!file || file.chunks.length) {
      return start();
    }
  };
  new_file = function() {
    restart();
    file["new"] = true;
    return file.from = '/dev/null';
  };
  deleted_file = function() {
    restart();
    file.deleted = true;
    return file.to = '/dev/null';
  };
  index = function(line) {
    restart();
    return file.index = line.split(' ').slice(1);
  };
  from_file = function(line) {
    restart();
    return file.from = parseFileFallback(line);
  };
  to_file = function(line) {
    restart();
    return file.to = parseFileFallback(line);
  };
  chunk = function(line, match) {
    var newLines, newStart, oldLines, oldStart;
    ln_del = oldStart = +match[1];
    oldLines = +(match[2] || 0);
    ln_add = newStart = +match[3];
    newLines = +(match[4] || 0);
    current = {
      content: line,
      changes: [],
      oldStart: oldStart,
      oldLines: oldLines,
      newStart: newStart,
      newLines: newLines
    };
    return file.chunks.push(current);
  };
  del = function(line) {
    current.changes.push({
      type: 'del',
      del: true,
      ln: ln_del++,
      content: line
    });
    return file.deletions++;
  };
  add = function(line) {
    current.changes.push({
      type: 'add',
      add: true,
      ln: ln_add++,
      content: line
    });
    return file.additions++;
  };
  noeol = '\\ No newline at end of file';
  normal = function(line) {
    if (!file) {
      return;
    }
    return current.changes.push({
      type: 'normal',
      normal: true,
      ln1: line !== noeol ? ln_del++ : void 0,
      ln2: line !== noeol ? ln_add++ : void 0,
      content: line
    });
  };
  schema = [[/^\s+/, normal], [/^diff\s/, start], [/^new file mode \d+$/, new_file], [/^deleted file mode \d+$/, deleted_file], [/^index\s[\da-zA-Z]+\.\.[\da-zA-Z]+(\s(\d+))?$/, index], [/^---\s/, from_file], [/^\+\+\+\s/, to_file], [/^@@\s+\-(\d+),?(\d+)?\s+\+(\d+),?(\d+)?\s@@/, chunk], [/^-/, del], [/^\+/, add]];
  parse = function(line) {
    var j, len, m, p;
    for (j = 0, len = schema.length; j < len; j++) {
      p = schema[j];
      m = line.match(p[0]);
      if (m) {
        p[1](line, m);
        return true;
      }
    }
    return false;
  };
  for (j = 0, len = lines.length; j < len; j++) {
    line = lines[j];
    parse(line);
  }
  return files;
};

parseFile = function(s) {
  var fileNames;
  if (!s) {
    return;
  }
  fileNames = s.split(' ').slice(-2);
  fileNames.map(function(fileName, i) {
    return fileNames[i] = fileName.replace(/^(a|b)\//, '');
  });
  return fileNames;
};

parseFileFallback = function(s) {
  var t;
  s = ltrim(s, '-');
  s = ltrim(s, '+');
  s = s.trim();
  t = /\t.*|\d{4}-\d\d-\d\d\s\d\d:\d\d:\d\d(.\d+)?\s(\+|-)\d\d\d\d/.exec(s);
  if (t) {
    s = s.substring(0, t.index).trim();
  }
  if (s.match(/^(a|b)\//)) {
    return s.substr(2);
  } else {
    return s;
  }
};

ltrim = function(s, chars) {
  s = makeString(s);
  if (!chars && trimLeft) {
    return trimLeft.call(s);
  }
  chars = defaultToWhiteSpace(chars);
  return s.replace(new RegExp('^' + chars + '+'), '');
};

makeString = function(s) {
  if (s === null) {
    return '';
  } else {
    return s + '';
  }
};

trimLeft = String.prototype.trimLeft;

defaultToWhiteSpace = function(chars) {
  if (chars === null) {
    return '\\s';
  }
  if (chars.source) {
    return chars.source;
  }
  return '[' + escapeRegExp(chars) + ']';
};

escapeRegExp = function(s) {
  return makeString(s).replace(/([.*+?^=!:${}()|[\]\/\\])/g, '\\$1');
};

},{}],2:[function(require,module,exports){
'use strict';
var _ = require('parse-diff');
window.parseDiff = _;

},{"parse-diff":1}]},{},[2]);
