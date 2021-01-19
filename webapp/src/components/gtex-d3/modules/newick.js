/*
 * Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
 * All rights reserved.
 */

export function parseNewick(s) {
    var ancestors = [];
    var tree = {};
    var tokens = s.split(/\s*(;|\(|\)|,|:)\s*/);
    for (let i = 0; i < tokens.length; i++) {
        let token = tokens[i];
        switch (token) {
            case '(': // new branchset
                var subtree = {};
                tree.branchset = [subtree];
                ancestors.push(tree);
                tree = subtree;
                break;
            case ',': // another branch
                var subtreea = {};
                ancestors[ancestors.length - 1].branchset.push(subtreea);
                tree = subtreea;
                break;
            case ')': // optional name next
                tree = ancestors.pop();
                break;
            case ':': // optional length next
                break;
            default:
                var x = tokens[i - 1];
                if (x === ')' || x === '(' || x === ',') {
                    tree.name = token;
                } else if (x === ':') {
                    tree.length = parseFloat(token);
                }
        }
    }
    return tree;
}

