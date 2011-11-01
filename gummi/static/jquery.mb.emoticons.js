
/*******************************************************************************
 jquery.mb.components
 Copyright (c) 2001-2010. Matteo Bicocchi (Pupunzi); Open lab srl, Firenze - Italy
 email: info@pupunzi.com
 site: http://pupunzi.com

 Licences: MIT, GPL
 http://www.opensource.org/licenses/mit-license.php
 http://www.gnu.org/licenses/gpl.html
 ******************************************************************************/

/*
 * Name:jquery.mb.emoticons
 * Version: 1.0
 */


(function($) {
  jQuery.mbEmoticons= {
    author:"Matteo Bicocchi",
    version:"1.0",
    smilesPath:"../static/",
    smiles: {
      "(angel)":      "angel",
      " :@":          "angry",
      "(bandit)":     "bandit",
      "(bear)":       "bear",
      "(beer)":       "beer",
      " :D":          "bigsmile",
      "(bow)":        "bow",
      "(u)":          "brokenheart",
      "(bug)":        "bug",
      "(^)":          "cake",
      "(call)":       "call",
      "(cash)":       "cash",
      "(clap)":       "clapping",
      "(coffee)":     "coffee",
      " 8-)":         "cool",
      " ;(":          "crying",
      "(dance)":      "dance",
      "(devil)":      "devil",
      "(doh)":        "doh",
      "(drink)":      "drink",
      "(drunk)":      "drunk",
      "(dull)":       "dull",
      "(blush)":      "eblush",
      "(emo)":        "emo",
      "(envy)":       "envy",
      " ]:)":         "evilgrin",
      "(F)":          "flower",
      "(fubar)":      "fubar",
      "(giggle)":     "giggle",
      "(handshake)":  "handshake",
      "(happy)":      "happy",
      "(headbang)":   "headbang",
      "(heart)":      "heart",
      "(heidy)":      "heidy",
      "(hi)":         "hi",
      "(inlove)":     "inlove",
      "(wasntme)":    "itwasntme",
      "(kiss)":       "kiss",
      " :x":          "lipssealed",
      "(mail)":       "mail",
      "(makeup)":     "makeup",
      "(finger)":     "middlefinger",
      "(mmm)":        "mmm",
      "(mooning)":    "mooning",
      "(~)":          "movie",
      "(muscle)":     "muscle",
      "(music)":      "music",
      "(myspace)":    "myspace",
      " 8-|":         "nerd",
      "(ninja)":      "ninja",
      "(no)":         "no",
      "(nod)":        "nod",
      "(party)":      "party",
      "(phone)":      "phone",
      "(pizza)":      "pizza",
      "(poolparty)":  "poolparty",
      "(puke)":       "puke",
      "(punch)":      "punch",
      "(rain)":       "rain",
      "(rock)":       "rock",
      "(rofl)":       "rofl",
      " :(":          "sadsmile",
      "(shake)":      "shake",
      "(skype)":      "skype",
      " |-)":         "sleepy",
      "(smile)":      "smile",
      "(smirk)":      "smirk",
      "(smoke)":      "smoke",
      " :|":          "speechless",
      "(*)":          "star",
      "(sun)":        "sun",
      " :O":          "surprised",
      "(swear)":      "swear",
      "(sweat)":   "sweating",
      "(talk)":       "talking",
      "(think)":      "thinking",
      "(o)":          "time",
      "(tmi)":        "tmi",
      "(toivo)":      "toivo",
      " :P":          "tongueout",
      "(wait)":       "wait",
      "(whew)":       "whew",
      "(wink)":       "wink",
      " :^)":         "wondering",
      " :S":          "worried",
      "(yawn)":       "yawn",
      "(yes)":        "yes"
    },
    smilesVariations: {
      ":-)": "smile",
      ":)": "smile"
    },
    smileBoxBtn:"#smileBoxBtn"
    ,
    getRegExp:function(){
      var ret="/";
      $.each($.mbEmoticons.smilesVariations,function(i){
        var emot= i.replace(/\)/g,"\\)").replace(/\(/g, "\\(").replace(/\|/g, "\\|").replace(/\*/g, "\\*").replace(/\^/g, "\\^");
        ret +="("+emot+")|";
      });
      ret+="/g";
      return eval(ret);
    },
    addSmilesBox:function(){
      $(this).each(function(){

        var textarea=$(this);

        var wrapper=$("<span/>").addClass("mbSmilesWrapper");
        textarea.wrapAll(wrapper);

        textarea.data("caret",textarea.caret());
        textarea.data("smilesIsOpen",true);
        var smilesBox=$("<div/>").addClass("mbSmilesBox").hide();
        var smilesButton=$("<span/>").addClass("mbSmilesButton").html(":-)").emoticonize();
        $.each($.mbEmoticons.smiles,function(i){
          var emoticon=$("<span/>").addClass("emoticon").html(i).attr("title",i);
          smilesBox.append(emoticon);
          emoticon.emoticonize().data("emoticon",i);
        });
        textarea.before(smilesButton);
        smilesButton.click(function(){
          textarea.mbOpenSmilesBox();
        });
        textarea.before(smilesBox);
        textarea.data("smilesBox",smilesBox);

        smilesBox.find(".emoticon").each(function(){
          var icon=$(this);
          $(this).hover(
                  function(){
                    var src= $(this).find("img").attr("src").replace(".png",".gif");
                    $(this).find("img").attr("src",src);
                  },
                  function(){
                    var src= $(this).find("img").attr("src").replace(".gif",".png");
                    $(this).find("img").attr("src",src);
                  })
                  .click(function(){
            textarea.insertAtCaret(" "+icon.data("emoticon")+" ");
          });
        });
        textarea.focus();
        textarea.caret(textarea.data("caret"));
      });
      return this;
    },

    openSmileBox:function(){
      var textarea = $(this);
      var smilesBox= textarea.data("smilesBox");
      var left= (textarea.position().left+(textarea.outerWidth()/2));
      smilesBox.css({left:left});
      smilesBox.fadeIn();
      setTimeout(function(){
        $(document).one("click",function(){textarea.mbCloseSmilesBox();});
      },100);
    },

    removeSmilesBox:function(){
      $(this).data("smilesIsOpen",false);
      var smilesBox= $(this).data("smilesBox");
      smilesBox.fadeOut(500);
    }
  };

  jQuery.fn.insertAtCaret = function (tagName) {
    return this.each(function(){
      if (document.selection) {
        //IE support
        this.focus();
        sel = document.selection.createRange();
        sel.text = tagName;
        this.focus();
      }else if (this.selectionStart || this.selectionStart == '0') {
        //MOZILLA/NETSCAPE support
        startPos = this.selectionStart;
        endPos = this.selectionEnd;
        scrollTop = this.scrollTop;
        this.value = this.value.substring(0, startPos) + tagName + this.value.substring(endPos,this.value.length);
        this.focus();
        this.selectionStart = startPos + tagName.length;
        this.selectionEnd = startPos + tagName.length;
        this.scrollTop = scrollTop;
      } else {
        this.value += tagName;
        this.focus();
      }
    });
  };

  jQuery.fn.caret = function(pos) {
    var target = this[0];
    if (arguments.length == 0) { //get
      if (target.selectionStart) { //DOM
        var pos = target.selectionStart;
        return pos > 0 ? pos : 0;
      }
      else if (target.createTextRange) { //IE
        target.focus();
        var range = document.selection.createRange();
        if (range == null)
          return '0';
        var re = target.createTextRange();
        var rc = re.duplicate();
        re.moveToBookmark(range.getBookmark());
        rc.setEndPoint('EndToStart', re);
        return rc.text.length;
      }
      else return 0;
    } //set
    if (target.setSelectionRange) //DOM
      target.setSelectionRange(pos, pos);
    else if (target.createTextRange) { //IE
      var range = target.createTextRange();
      range.collapse(true);
      range.moveEnd('character', pos);
      range.moveStart('character', pos);
      range.select();
    }
  };

  // variation from Roberto Bichierai emoticonize component.
  jQuery.fn.emoticonize = function (animate) {
    function convert (text){
      var icons = $.mbEmoticons.getRegExp();
      return text.replace (icons,function(str){
        var ret= $.mbEmoticons.smilesVariations[str];
        var ext=animate?".gif":".png";
        if (ret){
          ret="<img src='"+$.mbEmoticons.smilesPath+"smiley/"+ret+ext+"'>";
          return ret;
        }else{
          return str;
        }
      });
    }
    this.each(function() {
      var el = $(this);
      var html = convert(el.html()).replace(/\n/g,"<br>");
      el.html(html);
    });
    return this;
  };

  $.extend($.mbEmoticons.smilesVariations,$.mbEmoticons.smiles);

  jQuery.fn.mbSmilesBox= $.mbEmoticons.addSmilesBox;
  jQuery.fn.mbOpenSmilesBox= $.mbEmoticons.openSmileBox;
  jQuery.fn.mbCloseSmilesBox= $.mbEmoticons.removeSmilesBox;

})(jQuery);
