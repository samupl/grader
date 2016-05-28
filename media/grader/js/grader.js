var getLine = function getLine(change, side) {
    var types = {
        'normal': (side == 'left') ? change.ln2 : change.ln1,
        'add': change.ln,
        'del': change.ln
    };
    return types[change.type];
};


var getChangeClass = function getChangeClass(change) {
    var classes = {
        add: 'text-success',
        del: 'text-danger',
        normal: 'text-normal'
    };
    return classes[change.type];
};


var getLineDiff = function getLineDiff(change1, change2) {
    if (!change1 || !change2) return 0;

    var cls1 = {
        add: change1.ln,
        del: change1.ln,
        normal: change1.ln2
    };

    var cls2 = {
        add: change2.ln,
        del: change2.ln,
        normal: change2.ln1
    };

    return cls1[change1.type] - cls2[change2.type];
};


jQuery.fn.extend({
    getDiff: function getDiff() {
        var diff = this.data('diff');
        diff = JSON.parse('"' + diff.replace('"', '\\"') + '"')
        diff = window.parseDiff(diff);
        return diff;
    },

    formatDiff: function formatDiff() {
        var that = this;
        var diff = that.getDiff();
        var std = this.data('std');
        var changesets = [];
        $.each(diff, function (index, obj) {
            $.each(obj.chunks, function (chunk_index, chunk) {
                var changes = {left: [], right: [], chunk: chunk};
                $.each(chunk.changes, function (change_index, change) {
                    switch(change.type) {
                        case 'normal':
                            changes.left.push(change);
                            changes.right.push(change);
                            break;

                        case 'add':
                            changes.left.push(change);
                            break;

                        case 'del':
                            changes.right.push(change);
                            break;
                    }
                });
                changesets.push(changes);
            });
        });
        var $block = $('<div></div>').addClass('diff-block');
        $.each(changesets, function (index, changeset) {
            console.log('New changeset');

            var $table = $('<table></table>').addClass('table table-condensed table-bordered');

            var $thead = $('<thead></thead>');
            var $theadTr = $('<tr></tr>');
            var $theadTd = $('<td></td>');
            $theadTd.attr('colspan', 4).text(changeset.chunk.content);
            $('<span></span>').text(std).addClass('pull-right').appendTo($theadTd);
            $theadTd.appendTo($theadTr);
            $theadTr.appendTo($thead);
            $thead.appendTo($table);

            var $tbody = $('<tbody></tbody>');
            $table.appendTo($block);
            $tbody.appendTo($table);
            while (changeset.left.length || changeset.right.length) {
                var $tr = $('<tr></tr>');

                var change_left = null;
                var change_right = null;

                if (changeset.left.length > 0) change_left = changeset.left.shift();
                if (changeset.right.length > 0) change_right = changeset.right.shift();
                var $left_lineno = $('<td></td>').addClass('lineno');
                var $right_lineno = $('<td></td>').addClass('lineno');
                var $left_content = $('<td></td>').addClass('content');
                var $right_content = $('<td></td>').addClass('content');

                if (change_left) {
                    $left_lineno.text(getLine(change_left, 'left'));
                    $left_lineno.addClass(getChangeClass(change_left));
                    $left_content.text(change_left.content);
                    $left_content.addClass(getChangeClass(change_left));
                }

                if (change_right) {
                    $right_lineno.text(getLine(change_right, 'right')).addClass(getChangeClass(change_right));
                    $right_content.text(change_right.content).addClass(getChangeClass(change_right));
                }

                $left_lineno.appendTo($tr);
                $left_content.appendTo($tr);
                $right_lineno.appendTo($tr);
                $right_content.appendTo($tr);
                $tr.appendTo($tbody);

                // Correct line numbers
            }
        });
        $block.appendTo(that);
    }
});

$(window).load(function () {

    $('.task-affix').affix({
        offset: {
            top: function () {
                var top = $($('.task')[0]).offset().top - 15;
                return (this.top = top);
            },
            bottom: function () {
                return (this.bottom = $('.footer').outerHeight(true))
            }
        }
    });
    
    $('.scores-affix').affix({
        offset: {
            top: function () {
                var top = $($('.score')[0]).offset().top - 15;
                return (this.top = top);
            },
            bottom: function () {
                return (this.bottom = $('.footer').outerHeight(true))
            }
        }
    });

    $('.diff').formatDiff();

    $('.showResult').click(function () {
        var resultId = $(this).data('result-id');
        var $result = $('#result-' + resultId);
        var $icon = $(this).find('i.fa');
        if ($icon.hasClass('fa-eye')) {
            // Show
            $result.show();
            $icon.removeClass('fa-eye').addClass('fa-eye-slash');
        } else {
            // Hide
            $result.hide();
            $icon.removeClass('fa-eye-slash').addClass('fa-eye');
        }
    });
});