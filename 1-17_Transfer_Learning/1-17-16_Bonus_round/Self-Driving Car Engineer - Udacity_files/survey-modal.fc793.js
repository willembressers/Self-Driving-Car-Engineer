(window.webpackJsonp=window.webpackJsonp||[]).push([[10],{1755:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.SlidesProvider=t.SlidesConsumer=void 0;var r,o=n(1);var a=((r=o)&&r.__esModule?r:{default:r}).default.createContext();t.SlidesConsumer=a.Consumer,t.SlidesProvider=a.Provider},1811:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=n(1891);Object.defineProperty(t,"NextButton",{enumerable:!0,get:function(){return r.NextButton}}),Object.defineProperty(t,"PrevButton",{enumerable:!0,get:function(){return r.PrevButton}});var o=n(1892);Object.defineProperty(t,"Slides",{enumerable:!0,get:function(){return(e=o,e&&e.__esModule?e:{default:e}).default;var e}});var a=n(1896);Object.defineProperty(t,"Slide",{enumerable:!0,get:function(){return a.Slide}}),Object.defineProperty(t,"Body",{enumerable:!0,get:function(){return a.Body}}),Object.defineProperty(t,"Footer",{enumerable:!0,get:function(){return a.Footer}})},1891:function(e,t,n){"use strict";(function(e,r,o){Object.defineProperty(t,"__esModule",{value:!0}),t.PrevButton=t.NextButton=void 0;var a,i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},l=n(1757),u=(a=l)&&a.__esModule?a:{default:a},s=n(35),c=n(51),f=n(1755),d=n(12);var p=t.NextButton=function(t){return e.createElement(f.SlidesConsumer,null,(function(n){var o=n.nextSlide,a=n.slideIndex===n.slideCount-1,l=t.onNext,s=t.autoAdvance,c=l?function(){return r.resolve(l()).then((function(){return o()}))}:o;return s&&c(),e.createElement(u.default,i({},t,{variant:"primary",onClick:c,label:a&&t.label===(0,d.__)("Next")?(0,d.__)("Done"):t.label}))}))};p.displayName="onboarding/slides/_navigation/next-button",p.propTypes=o.omit(s.Button.propTypes,["type","onClick"]);var y=t.PrevButton=function(t){return e.createElement(f.SlidesConsumer,null,(function(n){var r=n.prevSlide;return n.slideIndex>0&&!t.disableBack&&e.createElement(s.Button,i({},t,{onClick:r,variant:"minimal",label:(0,d.__)("Back"),icon:e.createElement(c.IconArrowLeft,null)}))}))};y.displayName="onboarding/slides/_navigation/prev-button",y.propTypes=o.omit(s.Button.propTypes,["type","label","children","onClick"])}).call(this,n(1),n(11),n(6))},1892:function(e,t,n){"use strict";(function(e,r,o){Object.defineProperty(t,"__esModule",{value:!0});var a,i,l=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),u=p(n(1893)),s=p(n(0)),c=n(1755),f=p(n(93)),d=p(n(1895));function p(e){return e&&e.__esModule?e:{default:e}}var y=(i=a=function(t){function n(e){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,n);var t=function(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}(this,(n.__proto__||Object.getPrototypeOf(n)).call(this,e));return t.prevSlide=function(){t.setState((function(e){var t=e.slideIndex;return{slideIndex:Math.max(t-1,0)}}))},t.nextSlide=function(){if(t.state.slideIndex===t.state.slideCount-1)return t.props.onFinish();t.setState((function(e){var t=e.slideIndex,n=e.slideCount;return{slideIndex:Math.min(t+1,n-1)}}))},t.state={prevSlide:t.prevSlide,nextSlide:t.nextSlide,slideIndex:0},t}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(n,t),l(n,null,[{key:"getDerivedStateFromProps",value:function(t,n){var o=e.Children.count(r.compact(t.children));return o!==n.slideCount?{slideCount:o,slideIndex:Math.min(n.slideIndex,o-1),onEnterSlide:t.onEnterSlide||r.noop}:null}}]),l(n,[{key:"_renderSlide",value:function(){return e.Children.toArray(this.props.children)[this.state.slideIndex]}},{key:"render",value:function(){var t=this.props,n=t.title,r=t.stylePrefix;return e.createElement(c.SlidesProvider,{value:this.state},e.createElement("div",{styleName:(0,f.default)("slides",r)},e.createElement("div",null,e.createElement("h4",{styleName:"title"},n),e.createElement(u.default,null)),this._renderSlide()))}}]),n}(e.Component),a.displayName="onboarding/slides/_slides",a.propTypes={title:s.default.node,children:s.default.node,onFinish:s.default.func,onEnterSlide:s.default.func,stylePrefix:s.default.string},a.defaultProps={onFinish:r.noop,onEnterSlide:r.noop,title:null,children:null,stylePrefix:""},i);t.default=o(y,d.default,{allowMultiple:!0})}).call(this,n(1),n(6),n(10))},1893:function(e,t,n){"use strict";(function(e){Object.defineProperty(t,"__esModule",{value:!0});var r=i(n(0)),o=i(n(1)),a=n(1755);function i(e){return e&&e.__esModule?e:{default:e}}var l=e((function(e){var t=e.value,n=void 0===t?0:t;return o.default.createElement("div",{styleName:"progress"},o.default.createElement("p",{role:"progressbar","aria-valuenow":n,"aria-valuemin":"0","aria-valuemax":"100",style:{width:n+"%"}},n,"% complete"))}),i(n(1894)).default);l.displayName="onboarding/slides/_progress/progress-bar",l.propTypes={value:r.default.number};var u=function(){return o.default.createElement(a.SlidesConsumer,null,(function(e){var t,n,r=e.slideIndex,a=e.slideCount;return o.default.createElement(l,{value:(t=r,n=a,100*(0===n?0:(t+1)/n))})}))};u.displayName="onboarding/slides/_progress",u.propTypes={},t.default=u}).call(this,n(10))},1894:function(e,t,n){e.exports={progress:"_progress--progress--3dYri"}},1895:function(e,t,n){e.exports={slides:"_slides--slides--3T5FZ",title:"_slides--title--1gVKX",onboarding:"_slides--onboarding--3D5qM"}},1896:function(e,t,n){"use strict";(function(e,r){Object.defineProperty(t,"__esModule",{value:!0}),t.Slide=t.Footer=t.Body=void 0;var o,a,i,l=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),u=f(n(0)),s=n(1755),c=f(n(1897));function f(e){return e&&e.__esModule?e:{default:e}}function d(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function p(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}var y=t.Body=e((function(e){var t=e.children,n=e.className;return r.createElement("div",{styleName:"body",className:n},t)}),c.default,{errorWhenNotFound:!1});y.displayName="onboarding/slides/_slide/body";var h=t.Footer=e((function(e){var t=e.children,n=e.className;return r.createElement("div",{styleName:"footer",className:n},t)}),c.default,{errorWhenNotFound:!1});h.displayName="onboarding/slides/_slide/footer",y.propTypes=h.propTypes={children:u.default.node};var b=e(c.default)((i=a=function(e){function t(){return d(this,t),p(this,(t.__proto__||Object.getPrototypeOf(t)).apply(this,arguments))}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),l(t,[{key:"componentDidMount",value:function(){var e=this.props;(0,e.onEnterSlide)(e.name)}},{key:"render",value:function(){var e=this.props.children;return r.createElement("div",{styleName:"slide"},e)}}]),t}(r.Component),a.displayName="onboarding/slides/_slide/inner-slide",a.propTypes={onEnterSlide:u.default.func.isRequired,name:u.default.string.isRequired,children:u.default.node},o=i))||o,v=t.Slide=function(e){var t=e.children,n=e.name,o=void 0===n?"Slide":n;return r.createElement(s.SlidesConsumer,null,(function(e){var n=e.onEnterSlide;return r.createElement(b,{onEnterSlide:n,name:o},t)}))};v.displayName="onboarding/slides/_slide",v.propTypes={children:u.default.node,name:u.default.string},t.default=v}).call(this,n(10),n(1))},1897:function(e,t,n){e.exports={slide:"_slide--slide--146nd",body:"_slide--body--2z1vT",footer:"_slide--footer--13p7L"}},2028:function(e,t,n){"use strict";(function(e,r){Object.defineProperty(t,"__esModule",{value:!0}),t.OtherRadio=t.OtherCheckbox=void 0;var o,a=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),i=n(35),l=n(0),u=(o=l)&&o.__esModule?o:{default:o},s=n(1745);function c(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function f(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}function d(t){var n,o;return o=n=function(n){function o(){var e,t,n;c(this,o);for(var r=arguments.length,a=Array(r),i=0;i<r;i++)a[i]=arguments[i];return t=n=f(this,(e=o.__proto__||Object.getPrototypeOf(o)).call.apply(e,[this].concat(a))),n.state={value:""},n.handleInputChange=function(e){var t=e.target.checked,r=n.props.onInputChange;r(t?n.state.value:null)},n.handleTextChange=function(e){var t=e.target.value;(0,n.props.onTextChange)(t),n.setState({value:t})},f(n,t)}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(o,n),a(o,[{key:"render",value:function(){var n=this.props,o=n.defaultValue,a=n.label,l=n.id,u=this.state.value||o;return e.createElement(t,{id:l,checked:!r.isNil(o),onChange:this.handleInputChange,label:e.createElement("div",{styleName:"other-field"},e.createElement(i.TextInput,{id:r.snakeCase(a),label:a,hiddenLabel:!0,placeholder:s.SURVEY_TEXTS.OTHER_TEXT_INPUT,value:u,onChange:this.handleTextChange}))})}}]),o}(e.Component),n.propTypes={label:u.default.string,id:u.default.string,defaultValue:u.default.string,onTextChange:u.default.func,onInputChange:u.default.func},o}(t.OtherCheckbox=d(i.Checkbox)).displayName="survey/choices/other-checkbox",(t.OtherRadio=d(i.Radio)).displayName="survey/choices/other-radio"}).call(this,n(1),n(6))},2703:function(e,t,n){"use strict";(function(e,r,o){Object.defineProperty(t,"__esModule",{value:!0}),t.SurveyModal=void 0;var a,i,l,u,s=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},c=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),f=n(1745),d=n(35),p=n(114),y=S(n(103)),h=S(n(2704)),b=S(n(0)),v=S(n(2705)),m=n(1811),_=n(1755),E=n(12),g=S(n(2718)),O=S(n(345));function S(e){return e&&e.__esModule?e:{default:e}}function T(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function w(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function k(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}var R=function(){return e.createElement(_.SlidesConsumer,null,(function(t){var n=t.slideIndex,r=t.slideCount;return e.createElement("h1",{className:g.default["counts-title"]},n+1+" of "+r)}))},C=t.SurveyModal=(a=r(g.default,{allowMultiple:!0}),(0,O.default)(i=a((u=l=function(t){function n(){var t,r,a;w(this,n);for(var i=arguments.length,l=Array(i),u=0;u<i;u++)l[u]=arguments[u];return r=a=k(this,(t=n.__proto__||Object.getPrototypeOf(n)).call.apply(t,[this].concat(l))),a.state={isOpen:!0,isFinished:!1,showWelcomeSlide:!0,responses:{}},a.handleOnRequestClose=function(){var e=a.props,t=e.onDismissModal,n=e.updateSurveyStatus,r=e.track;n({status:status,time_stamp:(new Date).getTime()});var o=a.state.isFinished;r("Survey closed",{finishedSurvey:o}),n(o?{status:f.COMPLETED_SURVEY,time_stamp:(new Date).getTime()}:{status:f.ATTEMPTED_SURVEY,time_stamp:(new Date).getTime()}),t(),a.setState({isOpen:!1})},a.handleFinish=function(){y.default.track("Survey Submission",a.state.responses),a.setState({isFinished:!0})},a.onResponseSelected=function(e,t){a.setState({responses:s({},a.state.responses,T({},e,t))})},a.getResponse=function(e){return o.get(a.state,["responses",e],null)},a.renderQuestions=function(){var t=f.SURVEY_TEXTS.SURVEYS;return o.map(t,(function(n,r){return e.createElement(v.default,{key:r,survey:n,isLast:r===t.length-1,onResponseSelected:a.onResponseSelected,response:a.getResponse(n.question)})}))},a.renderContent=function(){var t=a.props.track,n=a.state,r=n.isFinished;return n.showWelcomeSlide?e.createElement("div",{styleName:"container"},e.createElement("h5",null,f.SURVEY_TEXTS.WELCOME_SURVEY_TITLE),e.createElement("h6",null,f.SURVEY_TEXTS.WELCOME_SURVEY_SUBTITLE),e.createElement(d.Button,{variant:"primary",label:(0,E.__)("Get started"),onClick:function(){return a.setState({showWelcomeSlide:!1})}})):r?e.createElement("div",{styleName:"container"},e.createElement("img",{src:h.default,alt:(0,E.__)("megaphone")}),e.createElement("span",{styleName:"thank-you-text"},(0,E.__)("Thank you!")),e.createElement(d.Button,{variant:"primary",label:(0,E.__)("Back to my course"),onClick:function(){return a.handleOnRequestClose()}})):e.createElement(m.Slides,{onEnterSlide:function(e){return t("Viewed "+e)},onFinish:a.handleFinish,title:e.createElement(R,null)},a.renderQuestions())},k(a,r)}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(n,t),c(n,[{key:"render",value:function(){var t=this.state.isOpen;return e.createElement(d.Modal,{open:t,onClose:this.handleOnRequestClose,label:(0,E.__)("Survey"),closeLabel:(0,E.__)("Close Modal")},this.renderContent())}}]),n}(e.Component),l.displayName="survey/survey-modal",l.propTypes={surveyEnabled:b.default.bool.isRequired,surveyStatus:b.default.object.isRequired,updateSurveyStatus:b.default.func,onDismissModal:b.default.func.isRequired,track:b.default.func.isRequired},i=u))||i)||i);t.default=(0,p.branch)((function(e){return!e.surveyEnabled}),p.renderNothing)(C)}).call(this,n(1),n(10),n(6))},2704:function(e,t,n){e.exports=n.p+"images/megaphone-49549.svg"},2705:function(e,t,n){"use strict";(function(e,r){Object.defineProperty(t,"__esModule",{value:!0}),t.QuestionSlide=void 0;var o,a,i,l=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),u=m(n(2706)),s=m(n(2708)),c=m(n(0)),f=m(n(2710)),d=m(n(2712)),p=m(n(2714)),y=m(n(2716)),h=n(1745),b=n(12),v=m(n(2717));function m(e){return e&&e.__esModule?e:{default:e}}function _(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function E(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}var g=t.QuestionSlide=e(v.default)((i=a=function(e){function t(){var e,n,r;_(this,t);for(var o=arguments.length,a=Array(o),i=0;i<o;i++)a[i]=arguments[i];return n=r=E(this,(e=t.__proto__||Object.getPrototypeOf(t)).call.apply(e,[this].concat(a))),r.handleResponseSelected=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:null,t=r.props,n=t.survey.question,o=t.onResponseSelected;o(n,e)},E(r,n)}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),l(t,[{key:"renderChoices",value:function(){var e=this.props,t=e.survey,n=t.question,o=t.answers,a=t.type,i=t.labels,l=t.range,c=t.categories,f=e.response;switch(a){case h.TYPES.RADIO:return r.createElement(d.default,{answers:o,onResponseSelected:this.handleResponseSelected,response:f});case h.TYPES.CHECKBOX:return r.createElement(s.default,{question:n,answers:o,onResponseSelected:this.handleResponseSelected,response:f});case h.TYPES.RATING:return r.createElement(p.default,{labels:i,range:l,onResponseSelected:this.handleResponseSelected,response:f});case h.TYPES.CATEGORY_RATING:return r.createElement(u.default,{categories:c,labels:i,range:l,onResponseSelected:this.handleResponseSelected,response:f});default:return null}}},{key:"render",value:function(){var e=this.props,t=e.survey,n=e.isLast;return r.createElement(f.default,{nextButtonLabel:n?(0,b.__)("Done"):(0,b.__)("Next")},r.createElement("h1",{styleName:"question-text"},t.question),r.createElement("div",{styleName:"answer-container"},this.renderChoices()))}}]),t}(r.Component),a.displayName="survey/question-slide",a.propTypes={survey:y.default.isRequired,isLast:c.default.bool,onResponseSelected:c.default.func,response:c.default.oneOfType([c.default.string,c.default.object,c.default.number])},a.defaultProps={isLast:!1},o=i))||o;t.default=g}).call(this,n(10),n(1))},2706:function(e,t,n){"use strict";(function(e,r,o){Object.defineProperty(t,"__esModule",{value:!0}),t.CategoryRankChoices=void 0;var a,i,l,u=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},s=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),c=n(35),f=h(n(0)),d=n(1745),p=n(12),y=h(n(2707));function h(e){return e&&e.__esModule?e:{default:e}}function b(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function v(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function m(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}var _=t.CategoryRankChoices=e(y.default,{allowMultiple:!0})((l=i=function(e){function t(){var e,n,r;v(this,t);for(var o=arguments.length,a=Array(o),i=0;i<o;i++)a[i]=arguments[i];return n=r=m(this,(e=t.__proto__||Object.getPrototypeOf(t)).call.apply(e,[this].concat(a))),r.handleRankSelected=function(e,t){r.props.onResponseSelected(u({},r.props.response,b({},t,e)))},m(r,n)}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),s(t,[{key:"renderCategoryRankChoices",value:function(e){var t=this;if(e===d.SURVEY_TEXTS.OTHER_TEXT_INPUT){var n=this.props.response;return r.createElement("div",{styleName:"other-input-container"},r.createElement("span",{styleName:"other-text"},d.SURVEY_TEXTS.OTHER_TEXT_INPUT,":"),r.createElement(c.TextInput,{label:d.SURVEY_TEXTS.OTHER_TEXT_INPUT,hiddenLabel:!0,value:o.get(n,"other"),placeholder:(0,p.__)("What else is important?"),onChange:function(e){return t.handleRankSelected(e.target.value,"other")}}))}return this.renderRanks(e)}},{key:"renderRanks",value:function(e){var t=this,n=this.props,a=n.range,i=n.response,l=o.get(i,e);return o.map(o.times(a),(function(n){var a=o.toString(n+1);return r.createElement(c.Button,{key:"choice-"+n,variant:l===a?"primary":"secondary",small:!0,label:a,onClick:function(){return t.handleRankSelected(a,e)}})}))}},{key:"renderLabels",value:function(){var e=this.props.labels;return o.map(e,(function(e){return r.createElement("span",{key:e,styleName:"label"},e)}))}},{key:"render",value:function(){var e=this,t=this.props.categories;return r.createElement("div",{styleName:"container"},o.map(t,(function(t){return r.createElement("div",{key:t,styleName:"category-container"},t!==d.SURVEY_TEXTS.OTHER_TEXT_INPUT&&r.createElement("span",{styleName:"category-title"},t),r.createElement("div",{styleName:"rank-container"},e.renderCategoryRankChoices(t)),t!==d.SURVEY_TEXTS.OTHER_TEXT_INPUT&&r.createElement("div",{styleName:"label-container"},e.renderLabels()))})))}}]),t}(r.Component),i.displayName="survey/choices/category-rank-choices",i.propTypes={categories:f.default.arrayOf(f.default.string).isRequired,range:f.default.number.isRequired,labels:f.default.arrayOf(f.default.string).isRequired,onResponseSelected:f.default.func.isRequired,response:f.default.objectOf(f.default.string)},a=l))||a;t.default=_}).call(this,n(10),n(1),n(6))},2707:function(e,t,n){e.exports={container:"category-rank-choices--container--27jgi","category-title":"category-rank-choices--category-title--1JOsR","rank-container":"category-rank-choices--rank-container--3ZhG0","label-container":"category-rank-choices--label-container--3GIVZ",label:"category-rank-choices--label--Sa4C-","other-input-container":"category-rank-choices--other-input-container--MrU1i","other-text":"category-rank-choices--other-text--19_nC","category-container":"category-rank-choices--category-container--1Wrdk"}},2708:function(e,t,n){"use strict";(function(e,r,o){Object.defineProperty(t,"__esModule",{value:!0}),t.CheckboxChoices=void 0;var a,i,l,u=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},s=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),c=n(35),f=n(2028),d=h(n(0)),p=n(1745),y=h(n(2709));function h(e){return e&&e.__esModule?e:{default:e}}function b(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function v(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function m(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}var _=t.CheckboxChoices=e(y.default)((l=i=function(e){function t(){return v(this,t),m(this,(t.__proto__||Object.getPrototypeOf(t)).apply(this,arguments))}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),s(t,[{key:"handleCheckboxSelected",value:function(e,t){var n=arguments.length>2&&void 0!==arguments[2]&&arguments[2],r=this.props,a=r.onResponseSelected,i=r.response,l=this.getNoneIndex(i);if(o.isEmpty(i)||e===p.SURVEY_TEXTS.NONE)a(b({},t,e));else if(i[t]!==e||n){if(-1!==l)return void a(b({},t,e));a(u({},i,b({},t,e)))}else a(o.omit(i,t))}},{key:"getNoneIndex",value:function(e){return o.indexOf(o.values(e),p.SURVEY_TEXTS.NONE)}},{key:"render",value:function(){var e=this,t=this.props,n=t.answers,a=t.response;return r.createElement("div",{styleName:"checkbox-container"},r.createElement("ul",{styleName:"answer-choices"},o.map(n,(function(t,n){if(t===p.SURVEY_TEXTS.OTHER_TEXT_INPUT){var i=o.get(a,n);return r.createElement("li",{key:n},r.createElement(f.OtherCheckbox,{id:n,label:p.SURVEY_TEXTS.OTHER_TEXT_INPUT,defaultValue:i,onTextChange:function(t){return e.handleCheckboxSelected(t,n,!0)},onInputChange:function(t){return e.handleCheckboxSelected(t,n)}}))}return r.createElement("li",{key:n},r.createElement(c.Checkbox,{id:n,checked:o.includes(a,t),label:t,onChange:function(){return e.handleCheckboxSelected(t,n)}}))}))))}}]),t}(r.Component),i.displayName="survey/choices/checkbox-choices",i.propTypes={answers:d.default.arrayOf(d.default.string).isRequired,onResponseSelected:d.default.func.isRequired,response:d.default.object},a=l))||a;t.default=_}).call(this,n(10),n(1),n(6))},2709:function(e,t,n){e.exports={"checkbox-container":"checkbox-choices--checkbox-container--1Vu_9","answer-choices":"checkbox-choices--answer-choices--Udo97 shared--answer-choices--2UYId"}},2710:function(e,t,n){"use strict";(function(e,r){Object.defineProperty(t,"__esModule",{value:!0});var o,a,i,l=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),u=n(1811),s=f(n(0)),c=n(12);function f(e){return e&&e.__esModule?e:{default:e}}function d(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function p(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}var y=e(f(n(2711)).default)((i=a=function(e){function t(){return d(this,t),p(this,(t.__proto__||Object.getPrototypeOf(t)).apply(this,arguments))}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),l(t,[{key:"render",value:function(){var e=this.props,t=e.children,n=e.nextButtonLabel;return r.createElement(u.Slide,null,r.createElement(u.Body,{styleName:"body"},r.createElement("div",{styleName:"content"},t)),r.createElement(u.Footer,null,r.createElement("div",{styleName:"footer-buttons"},r.createElement("div",null,r.createElement(u.PrevButton,null)),r.createElement(u.NextButton,{label:n}))))}}]),t}(r.Component),a.displayName="survey/question",a.propTypes={children:s.default.node,nextButtonLabel:s.default.string},a.defaultProps={get nextButtonLabel(){return(0,c.__)("Next")}},o=i))||o;t.default=y}).call(this,n(10),n(1))},2711:function(e,t,n){e.exports={content:"question--content--2wFoI","footer-buttons":"question--footer-buttons--18vjA",body:"question--body--k4d6E"}},2712:function(e,t,n){"use strict";(function(e,r,o){Object.defineProperty(t,"__esModule",{value:!0}),t.RadioChoices=void 0;var a,i,l,u=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),s=n(2028),c=h(n(0)),f=n(35),d=n(1745),p=n(12),y=h(n(2713));function h(e){return e&&e.__esModule?e:{default:e}}function b(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function v(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}var m=t.RadioChoices=e(y.default)((l=i=function(e){function t(){var e,n,r;b(this,t);for(var o=arguments.length,a=Array(o),i=0;i<o;i++)a[i]=arguments[i];return n=r=v(this,(e=t.__proto__||Object.getPrototypeOf(t)).call.apply(e,[this].concat(a))),r.handleSelectAnswer=function(e){var t=!(arguments.length>1&&void 0!==arguments[1])||arguments[1],n=r.props,o=n.onResponseSelected,a=n.response;return e===a&&t?o():o(e)},v(r,n)}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),u(t,[{key:"render",value:function(){var e=this,t=this.props,n=t.answers,a=t.response;return r.createElement("ul",{styleName:"answer-choices"},o.map(n,(function(t,i){if(o.isEqual(d.SURVEY_TEXTS.OTHER_TEXT_INPUT,t)){var l=o.includes(n,a)?null:a;return r.createElement("li",{key:i},r.createElement(s.OtherRadio,{id:i,label:d.SURVEY_TEXTS.OTHER_TEXT_INPUT,defaultValue:l,onInputChange:function(t){return e.handleSelectAnswer(t)},onTextChange:function(t){return e.handleSelectAnswer(t,!1)}}))}return r.createElement("li",{key:i},r.createElement(f.Radio,{checked:a===t,id:i,label:(0,p.__)(t),onChange:function(){return e.handleSelectAnswer(t)}}))})))}}]),t}(r.Component),i.displayName="survey/radio-choices",i.propTypes={answers:c.default.arrayOf(c.default.string).isRequired,onResponseSelected:c.default.func,response:c.default.object},a=l))||a;t.default=m}).call(this,n(10),n(1),n(6))},2713:function(e,t,n){e.exports={"choice-container":"radio-choices--choice-container--_Hx8z","answer-choices":"radio-choices--answer-choices--KXB11 shared--answer-choices--2UYId"}},2714:function(e,t,n){"use strict";(function(e,r,o){Object.defineProperty(t,"__esModule",{value:!0}),t.RankChoices=void 0;var a,i,l,u=function(e,t){if(Array.isArray(e))return e;if(Symbol.iterator in Object(e))return function(e,t){var n=[],r=!0,o=!1,a=void 0;try{for(var i,l=e[Symbol.iterator]();!(r=(i=l.next()).done)&&(n.push(i.value),!t||n.length!==t);r=!0);}catch(e){o=!0,a=e}finally{try{!r&&l.return&&l.return()}finally{if(o)throw a}}return n}(e,t);throw new TypeError("Invalid attempt to destructure non-iterable instance")},s=function(){function e(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}return function(t,n,r){return n&&e(t.prototype,n),r&&e(t,r),t}}(),c=n(35),f=p(n(0)),d=p(n(2715));function p(e){return e&&e.__esModule?e:{default:e}}function y(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function h(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}var b=t.RankChoices=e(d.default,{allowMultiple:!0})((l=i=function(e){function t(){var e,n,r;y(this,t);for(var o=arguments.length,a=Array(o),i=0;i<o;i++)a[i]=arguments[i];return n=r=h(this,(e=t.__proto__||Object.getPrototypeOf(t)).call.apply(e,[this].concat(a))),r.handleRankSelected=function(e){r.props.onResponseSelected(e)},h(r,n)}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,e),s(t,[{key:"renderRankChoices",value:function(){var e=this,t=this.props,n=t.range,a=t.response;return o.map(o.times(n),(function(t){var n=(t+1).toString();return r.createElement(c.Button,{key:"choice-"+t,variant:a===n?"primary":"secondary",small:!0,label:n,onClick:function(){return e.handleRankSelected(n)}})}))}},{key:"renderLabels",value:function(){var e=this.props.labels;return o.map(e,(function(e){return r.createElement("span",{key:e,styleName:"label"},e)}))}},{key:"render",value:function(){var e=u(this.props.labels,2),t=e[0],n=e[1];return r.createElement("div",{styleName:"container"},r.createElement("div",{styleName:"mobile-label"},r.createElement("span",{styleName:"label"},t)),r.createElement("div",{styleName:"rank-container"},this.renderRankChoices()),r.createElement("div",{styleName:"mobile-label"},r.createElement("span",{styleName:"label"},n)),r.createElement("div",{styleName:"label-container"},this.renderLabels()))}}]),t}(r.Component),i.displayName="survey/choices/rank-choices",i.propTypes={range:f.default.number.isRequired,labels:f.default.arrayOf(f.default.string).isRequired,onResponseSelected:f.default.func,response:f.default.object},a=l))||a;t.default=b}).call(this,n(10),n(1),n(6))},2715:function(e,t,n){e.exports={container:"rank-choices--container--2jhbj","label-container":"rank-choices--label-container--2ZwSK",label:"rank-choices--label--2L_SK","question-container":"rank-choices--question-container--L3R89","rank-container":"rank-choices--rank-container--3DZrI","mobile-label":"rank-choices--mobile-label--28FTi"}},2716:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r,o=n(0),a=(r=o)&&r.__esModule?r:{default:r};t.default=a.default.shape({question:a.default.string.isRequired,type:a.default.string.isRequired,answers:a.default.arrayOf(a.default.string),range:a.default.number,hasInput:a.default.bool})},2717:function(e,t,n){e.exports={"question-container":"question-slide--question-container--SqGeU","question-text":"question-slide--question-text--1rXoT","answer-container":"question-slide--answer-container--1-dV4"}},2718:function(e,t,n){e.exports={footer:"survey-modal--footer--2dsEa",container:"survey-modal--container--1uRoB","icon-container":"survey-modal--icon-container--38-v3","thank-you-text":"survey-modal--thank-you-text--2PpAq","counts-title":"survey-modal--counts-title--2bBbK","modal-sidebar":"survey-modal--modal-sidebar--gtlSc"}}}]);
//# sourceMappingURL=https://s3-us-west-2.amazonaws.com/udacity-classroom-web/js/survey-modal.fc793.js.map