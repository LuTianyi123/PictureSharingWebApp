$(function () {
    var oExports = {
        initialize: fInitialize,
        renderMore: fRenderMore,
        requestData: fRequestData,
        tpl: fTpl
    };
    oExports.initialize();

    function fInitialize() {
        var that = this;
        that.listEl = $('div.js-index-list');

        that.page = 1;
        that.pageSize = 10;
        that.listHasNext = true;

        $('.js-load-more').on('click', function (oEvent) {
            var oEl = $(oEvent.currentTarget);
            var sAttName = 'data-load';

            if (oEl.attr(sAttName) === '1') {
                return;
            }

            oEl.attr(sAttName, '1');
            that.renderMore(function () {

                oEl.removeAttr(sAttName);
                !that.listHasNext && oEl.hide();
            });
        });
    }

    function fRenderMore(fCb) {
        var that = this;

        if (!that.listHasNext) {
            return;
        }
        that.requestData({

            page: that.page + 1,
            pageSize: that.pageSize,
            call: function (oResult) {

                that.listHasNext = !!oResult.has_next && (oResult.images || []).length > 0;
                that.page++;
                var sHtml = '';
                $.each(oResult.images, function (nIndex, oImage) {
                    /*
                     sHtml += that.tpl([
                        '<a class="item" href="/image/#{id}">',
                            '<div class="img-box">',
                                '<img src="#{url}">',
                            '</div>',
                            '<div class="img-mask"></div>',
                            '<div class="interaction-wrap">',
                                '<div class="interaction-item"><i class="icon-comment"></i>#{comment_count}</div>',
                            '</div>',
                        '</a>'].join(''), oImage);
                    */

                     sHtml1 = that.tpl([
                         '<article class="mod">',
            '<header class="mod-hd">',
                '<time class="time">#{created_date}</time>',
                '<a href="/profile/#{image.user.id}" class="avatar">',
                 '   <img src="#{head_url}">',
                '</a>',
                '<div class="profile-info">',
                    '<a title="#{image_user_username}" href="/profile/#{user_id}">#{username}</a>',
                '</div>',
            '</header>',
            '<div class="mod-bd">',
                '<div class="img-box">',
                    '<a href="/image/#{id}">',
                    '<img img src="#{url}">',
               ' </div>',
           ' </div>',
           ' <div class="mod-ft">',
              '  <ul class="discuss-list">',
                   ' <li class="more-discuss">',
                       ' <a>',
                           ' <span>there are </span><span class="">#{comment_count}</span>',
                            '<span> comments </span></a>'
                        ].join(''), oImage);

                sHtml2 = '';
                for (var ni = 0; ni < oImage.image_comments_length; ni++){
                        dict = {'comment_user_username':oImage.comment_user_username[ni], 'comment_user_id':oImage.comment_user_id[ni],
                            'comment_content':oImage.comment_content[ni] };
                        sHtml_part2 += that.tpl([
                        '    <li>',
                            '    <a class="_4zhc5 _iqaka" title="#{comment_user_username}" href="/profile/#{user_id}" data-reactid=".0.1.0.0.0.2.1.2:$comment-17856951190001917.1">#{commentsusername}</a>',
                            '    <span>',
                            '        <span>#{comments}</span>',
                           '     </span>',
                         '   </li>',
                             ].join(''), dict);
                    }

                 sHtml3 =    that.tpl([
              '  </ul>',
               ' <section class="discuss-edit">',
                  '  <a class="icon-heart"></a>',
                  '  <form>',
                   '     <input placeholder="Comment" type="text">',
                  '  </form>',
                  '  <button class="more-info">鏇村閫夐」</button>',
               ' </section>',
           ' </div>',

       ' </article>  '
                    ].join(''), oImage);

                sHtml = sHtml1 + sHtml2 + sHtml3;
                sHtml && that.listEl.append(sHtml);
                     });
            },
            error: function () {
                alert('Please Try Again');
            },
            always: fCb
        });
    }

    function fRequestData(oConf) {
        var that = this;
        var sUrl = '/index/images/' + oConf.page + '/' + oConf.pageSize + '/';
        $.ajax({url: sUrl, dataType: 'json'}).done(oConf.call).fail(oConf.error).always(oConf.always);
    }

    function fTpl(sTpl, oData) {
        var that = this;
        sTpl = $.trim(sTpl);
        return sTpl.replace(/#{(.*?)}/g, function (sStr, sName) {
            return oData[sName] === undefined || oData[sName] === null ? '' : oData[sName];
        });
    }
});