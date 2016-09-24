$(function () {
    var oExports = {
        initialize: fInitialize,
        encode: fEncode
    };
    oExports.initialize();

    function fInitialize() {
        var that = this;
        var sImageId = window.imageId;
        var oCmtIpt = $('#jsCmt');
        var oListDv = $('ul.js-discuss-list');

        var bSubmit = false;
        $('#jsSubmit').on('click', function () {
            var sCmt = $.trim(oCmtIpt.val());

            if (!sCmt) {
                return alert('Comment should not be empty');
            }

            if (bSubmit) {
                return;
            }
            bSubmit = true;
            $.ajax({
                url: '/addcomment/',
                type: 'post',
                dataType: 'json',
                data: {image_id: sImageId, content: sCmt}
            }).done(function (oResult) {
                if (oResult.code !== 0) {
                    return alert(oResult.content || '提交失败，请重试');
                }

                oCmtIpt.val('');
                //
                var sHtml = [
                    '<li>',
                        '<a title="', that.encode(oResult.username), '">', that.encode(oResult.username), '</a> ',
                        '<span><span>', that.encode(oResult.content), '</span></span>',
                    '</li>'].join('');
                oListDv.prepend(sHtml);
            }).fail(function (oResult) {
                alert(oResult.content || 'Please Try Again');
            }).always(function () {
                bSubmit = false;
            });
        });
    }

    function fEncode(sStr, bDecode) {
        var aReplace =["&#39;", "'", "&quot;", '"', "&nbsp;", " ", "&gt;", ">", "&lt;", "<", "&amp;", "&", "&yen;", "¥"];
        !bDecode && aReplace.reverse();
        for (var i = 0, l = aReplace.length; i < l; i += 2) {
             sStr = sStr.replace(new RegExp(aReplace[i],'g'), aReplace[i+1]);
        }
        return sStr;
    };

});