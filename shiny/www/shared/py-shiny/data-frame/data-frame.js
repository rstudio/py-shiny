var Ae,
  h,
  pn,
  wo,
  _e,
  dn,
  mn,
  mt,
  _n,
  Ue = {},
  hn = [],
  Co = /acit|ex(?:s|g|n|p|$)|rph|grid|ows|mnc|ntw|ine[ch]|zoo|^ord|itera/i,
  qe = Array.isArray;
function le(e, n) {
  for (var t in n) e[t] = n[t];
  return e;
}
function vn(e) {
  var n = e.parentNode;
  n && n.removeChild(e);
}
function G(e, n, t) {
  var r,
    o,
    i,
    l = {};
  for (i in n)
    i == "key" ? (r = n[i]) : i == "ref" ? (o = n[i]) : (l[i] = n[i]);
  if (
    (arguments.length > 2 &&
      (l.children = arguments.length > 3 ? Ae.call(arguments, 2) : t),
    typeof e == "function" && e.defaultProps != null)
  )
    for (i in e.defaultProps) l[i] === void 0 && (l[i] = e.defaultProps[i]);
  return De(e, l, r, o, null);
}
function De(e, n, t, r, o) {
  var i = {
    type: e,
    props: n,
    key: t,
    ref: r,
    __k: null,
    __: null,
    __b: 0,
    __e: null,
    __d: void 0,
    __c: null,
    __h: null,
    constructor: void 0,
    __v: o ?? ++pn,
  };
  return o == null && h.vnode != null && h.vnode(i), i;
}
function ht() {
  return { current: null };
}
function te(e) {
  return e.children;
}
function W(e, n) {
  (this.props = e), (this.context = n);
}
function Oe(e, n) {
  if (n == null) return e.__ ? Oe(e.__, e.__.__k.indexOf(e) + 1) : null;
  for (var t; n < e.__k.length; n++)
    if ((t = e.__k[n]) != null && t.__e != null) return t.__e;
  return typeof e.type == "function" ? Oe(e) : null;
}
function yn(e) {
  var n, t;
  if ((e = e.__) != null && e.__c != null) {
    for (e.__e = e.__c.base = null, n = 0; n < e.__k.length; n++)
      if ((t = e.__k[n]) != null && t.__e != null) {
        e.__e = e.__c.base = t.__e;
        break;
      }
    return yn(e);
  }
}
function _t(e) {
  ((!e.__d && (e.__d = !0) && _e.push(e) && !je.__r++) ||
    dn !== h.debounceRendering) &&
    ((dn = h.debounceRendering) || mn)(je);
}
function je() {
  var e, n, t, r, o, i, l, u;
  for (_e.sort(mt); (e = _e.shift()); )
    e.__d &&
      ((n = _e.length),
      (r = void 0),
      (o = void 0),
      (l = (i = (t = e).__v).__e),
      (u = t.__P) &&
        ((r = []),
        ((o = le({}, i)).__v = i.__v + 1),
        vt(
          u,
          i,
          o,
          t.__n,
          u.ownerSVGElement !== void 0,
          i.__h != null ? [l] : null,
          r,
          l ?? Oe(i),
          i.__h
        ),
        En(r, i),
        i.__e != l && yn(i)),
      _e.length > n && _e.sort(mt));
  je.__r = 0;
}
function bn(e, n, t, r, o, i, l, u, a, d) {
  var s,
    g,
    f,
    c,
    p,
    m,
    _,
    v = (r && r.__k) || hn,
    w = v.length;
  for (t.__k = [], s = 0; s < n.length; s++)
    if (
      (c = t.__k[s] =
        (c = n[s]) == null || typeof c == "boolean" || typeof c == "function"
          ? null
          : typeof c == "string" || typeof c == "number" || typeof c == "bigint"
          ? De(null, c, null, null, c)
          : qe(c)
          ? De(te, { children: c }, null, null, null)
          : c.__b > 0
          ? De(c.type, c.props, c.key, c.ref ? c.ref : null, c.__v)
          : c) != null
    ) {
      if (
        ((c.__ = t),
        (c.__b = t.__b + 1),
        (f = v[s]) === null || (f && c.key == f.key && c.type === f.type))
      )
        v[s] = void 0;
      else
        for (g = 0; g < w; g++) {
          if ((f = v[g]) && c.key == f.key && c.type === f.type) {
            v[g] = void 0;
            break;
          }
          f = null;
        }
      vt(e, c, (f = f || Ue), o, i, l, u, a, d),
        (p = c.__e),
        (g = c.ref) &&
          f.ref != g &&
          (_ || (_ = []),
          f.ref && _.push(f.ref, null, c),
          _.push(g, c.__c || p, c)),
        p != null
          ? (m == null && (m = p),
            typeof c.type == "function" && c.__k === f.__k
              ? (c.__d = a = Sn(c, a, e))
              : (a = wn(e, c, f, v, p, a)),
            typeof t.type == "function" && (t.__d = a))
          : a && f.__e == a && a.parentNode != e && (a = Oe(f));
    }
  for (t.__e = m, s = w; s--; )
    v[s] != null &&
      (typeof t.type == "function" &&
        v[s].__e != null &&
        v[s].__e == t.__d &&
        (t.__d = Cn(r).nextSibling),
      xn(v[s], v[s]));
  if (_) for (s = 0; s < _.length; s++) Rn(_[s], _[++s], _[++s]);
}
function Sn(e, n, t) {
  for (var r, o = e.__k, i = 0; o && i < o.length; i++)
    (r = o[i]) &&
      ((r.__ = e),
      (n =
        typeof r.type == "function" ? Sn(r, n, t) : wn(t, r, r, o, r.__e, n)));
  return n;
}
function ne(e, n) {
  return (
    (n = n || []),
    e == null ||
      typeof e == "boolean" ||
      (qe(e)
        ? e.some(function (t) {
            ne(t, n);
          })
        : n.push(e)),
    n
  );
}
function wn(e, n, t, r, o, i) {
  var l, u, a;
  if (n.__d !== void 0) (l = n.__d), (n.__d = void 0);
  else if (t == null || o != i || o.parentNode == null)
    e: if (i == null || i.parentNode !== e) e.appendChild(o), (l = null);
    else {
      for (u = i, a = 0; (u = u.nextSibling) && a < r.length; a += 1)
        if (u == o) break e;
      e.insertBefore(o, i), (l = i);
    }
  return l !== void 0 ? l : o.nextSibling;
}
function Cn(e) {
  var n, t, r;
  if (e.type == null || typeof e.type == "string") return e.__e;
  if (e.__k) {
    for (n = e.__k.length - 1; n >= 0; n--)
      if ((t = e.__k[n]) && (r = Cn(t))) return r;
  }
  return null;
}
function Eo(e, n, t, r, o) {
  var i;
  for (i in t)
    i === "children" || i === "key" || i in n || Ke(e, i, null, t[i], r);
  for (i in n)
    (o && typeof n[i] != "function") ||
      i === "children" ||
      i === "key" ||
      i === "value" ||
      i === "checked" ||
      t[i] === n[i] ||
      Ke(e, i, n[i], t[i], r);
}
function cn(e, n, t) {
  n[0] === "-"
    ? e.setProperty(n, t ?? "")
    : (e[n] =
        t == null ? "" : typeof t != "number" || Co.test(n) ? t : t + "px");
}
function Ke(e, n, t, r, o) {
  var i;
  e: if (n === "style")
    if (typeof t == "string") e.style.cssText = t;
    else {
      if ((typeof r == "string" && (e.style.cssText = r = ""), r))
        for (n in r) (t && n in t) || cn(e.style, n, "");
      if (t) for (n in t) (r && t[n] === r[n]) || cn(e.style, n, t[n]);
    }
  else if (n[0] === "o" && n[1] === "n")
    (i = n !== (n = n.replace(/Capture$/, ""))),
      (n = n.toLowerCase() in e ? n.toLowerCase().slice(2) : n.slice(2)),
      e.l || (e.l = {}),
      (e.l[n + i] = t),
      t
        ? r || e.addEventListener(n, i ? gn : fn, i)
        : e.removeEventListener(n, i ? gn : fn, i);
  else if (n !== "dangerouslySetInnerHTML") {
    if (o) n = n.replace(/xlink(H|:h)/, "h").replace(/sName$/, "s");
    else if (
      n !== "width" &&
      n !== "height" &&
      n !== "href" &&
      n !== "list" &&
      n !== "form" &&
      n !== "tabIndex" &&
      n !== "download" &&
      n !== "rowSpan" &&
      n !== "colSpan" &&
      n in e
    )
      try {
        e[n] = t ?? "";
        break e;
      } catch {}
    typeof t == "function" ||
      (t == null || (t === !1 && n[4] !== "-")
        ? e.removeAttribute(n)
        : e.setAttribute(n, t));
  }
}
function fn(e) {
  return this.l[e.type + !1](h.event ? h.event(e) : e);
}
function gn(e) {
  return this.l[e.type + !0](h.event ? h.event(e) : e);
}
function vt(e, n, t, r, o, i, l, u, a) {
  var d,
    s,
    g,
    f,
    c,
    p,
    m,
    _,
    v,
    w,
    x,
    M,
    I,
    N,
    J,
    O = n.type;
  if (n.constructor !== void 0) return null;
  t.__h != null &&
    ((a = t.__h), (u = n.__e = t.__e), (n.__h = null), (i = [u])),
    (d = h.__b) && d(n);
  try {
    e: if (typeof O == "function") {
      if (
        ((_ = n.props),
        (v = (d = O.contextType) && r[d.__c]),
        (w = d ? (v ? v.props.value : d.__) : r),
        t.__c
          ? (m = (s = n.__c = t.__c).__ = s.__E)
          : ("prototype" in O && O.prototype.render
              ? (n.__c = s = new O(_, w))
              : ((n.__c = s = new W(_, w)),
                (s.constructor = O),
                (s.render = xo)),
            v && v.sub(s),
            (s.props = _),
            s.state || (s.state = {}),
            (s.context = w),
            (s.__n = r),
            (g = s.__d = !0),
            (s.__h = []),
            (s._sb = [])),
        s.__s == null && (s.__s = s.state),
        O.getDerivedStateFromProps != null &&
          (s.__s == s.state && (s.__s = le({}, s.__s)),
          le(s.__s, O.getDerivedStateFromProps(_, s.__s))),
        (f = s.props),
        (c = s.state),
        (s.__v = n),
        g)
      )
        O.getDerivedStateFromProps == null &&
          s.componentWillMount != null &&
          s.componentWillMount(),
          s.componentDidMount != null && s.__h.push(s.componentDidMount);
      else {
        if (
          (O.getDerivedStateFromProps == null &&
            _ !== f &&
            s.componentWillReceiveProps != null &&
            s.componentWillReceiveProps(_, w),
          (!s.__e &&
            s.shouldComponentUpdate != null &&
            s.shouldComponentUpdate(_, s.__s, w) === !1) ||
            n.__v === t.__v)
        ) {
          for (
            n.__v !== t.__v && ((s.props = _), (s.state = s.__s), (s.__d = !1)),
              s.__e = !1,
              n.__e = t.__e,
              n.__k = t.__k,
              n.__k.forEach(function (ce) {
                ce && (ce.__ = n);
              }),
              x = 0;
            x < s._sb.length;
            x++
          )
            s.__h.push(s._sb[x]);
          (s._sb = []), s.__h.length && l.push(s);
          break e;
        }
        s.componentWillUpdate != null && s.componentWillUpdate(_, s.__s, w),
          s.componentDidUpdate != null &&
            s.__h.push(function () {
              s.componentDidUpdate(f, c, p);
            });
      }
      if (
        ((s.context = w),
        (s.props = _),
        (s.__P = e),
        (M = h.__r),
        (I = 0),
        "prototype" in O && O.prototype.render)
      ) {
        for (
          s.state = s.__s,
            s.__d = !1,
            M && M(n),
            d = s.render(s.props, s.state, s.context),
            N = 0;
          N < s._sb.length;
          N++
        )
          s.__h.push(s._sb[N]);
        s._sb = [];
      } else
        do
          (s.__d = !1),
            M && M(n),
            (d = s.render(s.props, s.state, s.context)),
            (s.state = s.__s);
        while (s.__d && ++I < 25);
      (s.state = s.__s),
        s.getChildContext != null && (r = le(le({}, r), s.getChildContext())),
        g ||
          s.getSnapshotBeforeUpdate == null ||
          (p = s.getSnapshotBeforeUpdate(f, c)),
        bn(
          e,
          qe(
            (J =
              d != null && d.type === te && d.key == null
                ? d.props.children
                : d)
          )
            ? J
            : [J],
          n,
          t,
          r,
          o,
          i,
          l,
          u,
          a
        ),
        (s.base = n.__e),
        (n.__h = null),
        s.__h.length && l.push(s),
        m && (s.__E = s.__ = null),
        (s.__e = !1);
    } else
      i == null && n.__v === t.__v
        ? ((n.__k = t.__k), (n.__e = t.__e))
        : (n.__e = Ro(t.__e, n, t, r, o, i, l, a));
    (d = h.diffed) && d(n);
  } catch (ce) {
    (n.__v = null),
      (a || i != null) &&
        ((n.__e = u), (n.__h = !!a), (i[i.indexOf(u)] = null)),
      h.__e(ce, n, t);
  }
}
function En(e, n) {
  h.__c && h.__c(n, e),
    e.some(function (t) {
      try {
        (e = t.__h),
          (t.__h = []),
          e.some(function (r) {
            r.call(t);
          });
      } catch (r) {
        h.__e(r, t.__v);
      }
    });
}
function Ro(e, n, t, r, o, i, l, u) {
  var a,
    d,
    s,
    g = t.props,
    f = n.props,
    c = n.type,
    p = 0;
  if ((c === "svg" && (o = !0), i != null)) {
    for (; p < i.length; p++)
      if (
        (a = i[p]) &&
        "setAttribute" in a == !!c &&
        (c ? a.localName === c : a.nodeType === 3)
      ) {
        (e = a), (i[p] = null);
        break;
      }
  }
  if (e == null) {
    if (c === null) return document.createTextNode(f);
    (e = o
      ? document.createElementNS("http://www.w3.org/2000/svg", c)
      : document.createElement(c, f.is && f)),
      (i = null),
      (u = !1);
  }
  if (c === null) g === f || (u && e.data === f) || (e.data = f);
  else {
    if (
      ((i = i && Ae.call(e.childNodes)),
      (d = (g = t.props || Ue).dangerouslySetInnerHTML),
      (s = f.dangerouslySetInnerHTML),
      !u)
    ) {
      if (i != null)
        for (g = {}, p = 0; p < e.attributes.length; p++)
          g[e.attributes[p].name] = e.attributes[p].value;
      (s || d) &&
        ((s && ((d && s.__html == d.__html) || s.__html === e.innerHTML)) ||
          (e.innerHTML = (s && s.__html) || ""));
    }
    if ((Eo(e, f, g, o, u), s)) n.__k = [];
    else if (
      (bn(
        e,
        qe((p = n.props.children)) ? p : [p],
        n,
        t,
        r,
        o && c !== "foreignObject",
        i,
        l,
        i ? i[0] : t.__k && Oe(t, 0),
        u
      ),
      i != null)
    )
      for (p = i.length; p--; ) i[p] != null && vn(i[p]);
    u ||
      ("value" in f &&
        (p = f.value) !== void 0 &&
        (p !== e.value ||
          (c === "progress" && !p) ||
          (c === "option" && p !== g.value)) &&
        Ke(e, "value", p, g.value, !1),
      "checked" in f &&
        (p = f.checked) !== void 0 &&
        p !== e.checked &&
        Ke(e, "checked", p, g.checked, !1));
  }
  return e;
}
function Rn(e, n, t) {
  try {
    typeof e == "function" ? e(n) : (e.current = n);
  } catch (r) {
    h.__e(r, t);
  }
}
function xn(e, n, t) {
  var r, o;
  if (
    (h.unmount && h.unmount(e),
    (r = e.ref) && ((r.current && r.current !== e.__e) || Rn(r, null, n)),
    (r = e.__c) != null)
  ) {
    if (r.componentWillUnmount)
      try {
        r.componentWillUnmount();
      } catch (i) {
        h.__e(i, n);
      }
    (r.base = r.__P = null), (e.__c = void 0);
  }
  if ((r = e.__k))
    for (o = 0; o < r.length; o++)
      r[o] && xn(r[o], n, t || typeof e.type != "function");
  t || e.__e == null || vn(e.__e), (e.__ = e.__e = e.__d = void 0);
}
function xo(e, n, t) {
  return this.constructor(e, t);
}
function Ce(e, n, t) {
  var r, o, i;
  h.__ && h.__(e, n),
    (o = (r = typeof t == "function") ? null : (t && t.__k) || n.__k),
    (i = []),
    vt(
      n,
      (e = ((!r && t) || n).__k = G(te, null, [e])),
      o || Ue,
      Ue,
      n.ownerSVGElement !== void 0,
      !r && t ? [t] : o ? null : n.firstChild ? Ae.call(n.childNodes) : null,
      i,
      !r && t ? t : o ? o.__e : n.firstChild,
      r
    ),
    En(i, e);
}
function yt(e, n) {
  Ce(e, n, yt);
}
function Fn(e, n, t) {
  var r,
    o,
    i,
    l,
    u = le({}, e.props);
  for (i in (e.type && e.type.defaultProps && (l = e.type.defaultProps), n))
    i == "key"
      ? (r = n[i])
      : i == "ref"
      ? (o = n[i])
      : (u[i] = n[i] === void 0 && l !== void 0 ? l[i] : n[i]);
  return (
    arguments.length > 2 &&
      (u.children = arguments.length > 3 ? Ae.call(arguments, 2) : t),
    De(e.type, u, r || e.key, o || e.ref, null)
  );
}
function bt(e, n) {
  var t = {
    __c: (n = "__cC" + _n++),
    __: e,
    Consumer: function (r, o) {
      return r.children(o);
    },
    Provider: function (r) {
      var o, i;
      return (
        this.getChildContext ||
          ((o = []),
          ((i = {})[n] = this),
          (this.getChildContext = function () {
            return i;
          }),
          (this.shouldComponentUpdate = function (l) {
            this.props.value !== l.value &&
              o.some(function (u) {
                (u.__e = !0), _t(u);
              });
          }),
          (this.sub = function (l) {
            o.push(l);
            var u = l.componentWillUnmount;
            l.componentWillUnmount = function () {
              o.splice(o.indexOf(l), 1), u && u.call(l);
            };
          })),
        r.children
      );
    },
  };
  return (t.Provider.__ = t.Consumer.contextType = t);
}
(Ae = hn.slice),
  (h = {
    __e: function (e, n, t, r) {
      for (var o, i, l; (n = n.__); )
        if ((o = n.__c) && !o.__)
          try {
            if (
              ((i = o.constructor) &&
                i.getDerivedStateFromError != null &&
                (o.setState(i.getDerivedStateFromError(e)), (l = o.__d)),
              o.componentDidCatch != null &&
                (o.componentDidCatch(e, r || {}), (l = o.__d)),
              l)
            )
              return (o.__E = o);
          } catch (u) {
            e = u;
          }
      throw e;
    },
  }),
  (pn = 0),
  (wo = function (e) {
    return e != null && e.constructor === void 0;
  }),
  (W.prototype.setState = function (e, n) {
    var t;
    (t =
      this.__s != null && this.__s !== this.state
        ? this.__s
        : (this.__s = le({}, this.state))),
      typeof e == "function" && (e = e(le({}, t), this.props)),
      e && le(t, e),
      e != null && this.__v && (n && this._sb.push(n), _t(this));
  }),
  (W.prototype.forceUpdate = function (e) {
    this.__v && ((this.__e = !0), e && this.__h.push(e), _t(this));
  }),
  (W.prototype.render = te),
  (_e = []),
  (mn =
    typeof Promise == "function"
      ? Promise.prototype.then.bind(Promise.resolve())
      : setTimeout),
  (mt = function (e, n) {
    return e.__v.__b - n.__v.__b;
  }),
  (je.__r = 0),
  (_n = 0);
var ge,
  V,
  St,
  Mn,
  Ee = 0,
  An = [],
  We = [],
  $n = h.__b,
  Vn = h.__r,
  In = h.diffed,
  Tn = h.__c,
  Dn = h.unmount;
function Re(e, n) {
  h.__h && h.__h(V, e, Ee || n), (Ee = 0);
  var t = V.__H || (V.__H = { __: [], __h: [] });
  return e >= t.__.length && t.__.push({ __V: We }), t.__[e];
}
function D(e) {
  return (Ee = 1), xe(Ln, e);
}
function xe(e, n, t) {
  var r = Re(ge++, 2);
  if (
    ((r.t = e),
    !r.__c &&
      ((r.__ = [
        t ? t(n) : Ln(void 0, n),
        function (u) {
          var a = r.__N ? r.__N[0] : r.__[0],
            d = r.t(a, u);
          a !== d && ((r.__N = [d, r.__[1]]), r.__c.setState({}));
        },
      ]),
      (r.__c = V),
      !V.u))
  ) {
    var o = function (u, a, d) {
      if (!r.__c.__H) return !0;
      var s = r.__c.__H.__.filter(function (f) {
        return f.__c;
      });
      if (
        s.every(function (f) {
          return !f.__N;
        })
      )
        return !i || i.call(this, u, a, d);
      var g = !1;
      return (
        s.forEach(function (f) {
          if (f.__N) {
            var c = f.__[0];
            (f.__ = f.__N), (f.__N = void 0), c !== f.__[0] && (g = !0);
          }
        }),
        !(!g && r.__c.props === u) && (!i || i.call(this, u, a, d))
      );
    };
    V.u = !0;
    var i = V.shouldComponentUpdate,
      l = V.componentWillUpdate;
    (V.componentWillUpdate = function (u, a, d) {
      if (this.__e) {
        var s = i;
        (i = void 0), o(u, a, d), (i = s);
      }
      l && l.call(this, u, a, d);
    }),
      (V.shouldComponentUpdate = o);
  }
  return r.__N || r.__;
}
function L(e, n) {
  var t = Re(ge++, 3);
  !h.__s && Ct(t.__H, n) && ((t.__ = e), (t.i = n), V.__H.__h.push(t));
}
function re(e, n) {
  var t = Re(ge++, 4);
  !h.__s && Ct(t.__H, n) && ((t.__ = e), (t.i = n), V.__h.push(t));
}
function B(e) {
  return (
    (Ee = 5),
    oe(function () {
      return { current: e };
    }, [])
  );
}
function Nn(e, n, t) {
  (Ee = 6),
    re(
      function () {
        return typeof e == "function"
          ? (e(n()),
            function () {
              return e(null);
            })
          : e
          ? ((e.current = n()),
            function () {
              return (e.current = null);
            })
          : void 0;
      },
      t == null ? t : t.concat(e)
    );
}
function oe(e, n) {
  var t = Re(ge++, 7);
  return Ct(t.__H, n) ? ((t.__V = e()), (t.i = n), (t.__h = e), t.__V) : t.__;
}
function se(e, n) {
  return (
    (Ee = 8),
    oe(function () {
      return e;
    }, n)
  );
}
function Pn(e) {
  var n = V.context[e.__c],
    t = Re(ge++, 9);
  return (
    (t.c = e),
    n ? (t.__ == null && ((t.__ = !0), n.sub(V)), n.props.value) : e.__
  );
}
function kn(e, n) {
  h.useDebugValue && h.useDebugValue(n ? n(e) : e);
}
function Hn() {
  var e = Re(ge++, 11);
  if (!e.__) {
    for (var n = V.__v; n !== null && !n.__m && n.__ !== null; ) n = n.__;
    var t = n.__m || (n.__m = [0, 0]);
    e.__ = "P" + t[0] + "-" + t[1]++;
  }
  return e.__;
}
function Fo() {
  for (var e; (e = An.shift()); )
    if (e.__P && e.__H)
      try {
        e.__H.__h.forEach(Xe), e.__H.__h.forEach(wt), (e.__H.__h = []);
      } catch (n) {
        (e.__H.__h = []), h.__e(n, e.__v);
      }
}
(h.__b = function (e) {
  (V = null), $n && $n(e);
}),
  (h.__r = function (e) {
    Vn && Vn(e), (ge = 0);
    var n = (V = e.__c).__H;
    n &&
      (St === V
        ? ((n.__h = []),
          (V.__h = []),
          n.__.forEach(function (t) {
            t.__N && (t.__ = t.__N), (t.__V = We), (t.__N = t.i = void 0);
          }))
        : (n.__h.forEach(Xe), n.__h.forEach(wt), (n.__h = []), (ge = 0))),
      (St = V);
  }),
  (h.diffed = function (e) {
    In && In(e);
    var n = e.__c;
    n &&
      n.__H &&
      (n.__H.__h.length &&
        ((An.push(n) !== 1 && Mn === h.requestAnimationFrame) ||
          ((Mn = h.requestAnimationFrame) || Mo)(Fo)),
      n.__H.__.forEach(function (t) {
        t.i && (t.__H = t.i),
          t.__V !== We && (t.__ = t.__V),
          (t.i = void 0),
          (t.__V = We);
      })),
      (St = V = null);
  }),
  (h.__c = function (e, n) {
    n.some(function (t) {
      try {
        t.__h.forEach(Xe),
          (t.__h = t.__h.filter(function (r) {
            return !r.__ || wt(r);
          }));
      } catch (r) {
        n.some(function (o) {
          o.__h && (o.__h = []);
        }),
          (n = []),
          h.__e(r, t.__v);
      }
    }),
      Tn && Tn(e, n);
  }),
  (h.unmount = function (e) {
    Dn && Dn(e);
    var n,
      t = e.__c;
    t &&
      t.__H &&
      (t.__H.__.forEach(function (r) {
        try {
          Xe(r);
        } catch (o) {
          n = o;
        }
      }),
      (t.__H = void 0),
      n && h.__e(n, t.__v));
  });
var On = typeof requestAnimationFrame == "function";
function Mo(e) {
  var n,
    t = function () {
      clearTimeout(r), On && cancelAnimationFrame(n), setTimeout(e);
    },
    r = setTimeout(t, 100);
  On && (n = requestAnimationFrame(t));
}
function Xe(e) {
  var n = V,
    t = e.__c;
  typeof t == "function" && ((e.__c = void 0), t()), (V = n);
}
function wt(e) {
  var n = V;
  (e.__c = e.__()), (V = n);
}
function Ct(e, n) {
  return (
    !e ||
    e.length !== n.length ||
    n.some(function (t, r) {
      return t !== e[r];
    })
  );
}
function Ln(e, n) {
  return typeof n == "function" ? n(e) : n;
}
function Xn(e, n) {
  for (var t in n) e[t] = n[t];
  return e;
}
function Rt(e, n) {
  for (var t in e) if (t !== "__source" && !(t in n)) return !0;
  for (var r in n) if (r !== "__source" && e[r] !== n[r]) return !0;
  return !1;
}
function Et(e, n) {
  return (e === n && (e !== 0 || 1 / e == 1 / n)) || (e != e && n != n);
}
function xt(e) {
  this.props = e;
}
function $o(e, n) {
  function t(o) {
    var i = this.props.ref,
      l = i == o.ref;
    return (
      !l && i && (i.call ? i(null) : (i.current = null)),
      n ? !n(this.props, o) || !l : Rt(this.props, o)
    );
  }
  function r(o) {
    return (this.shouldComponentUpdate = t), G(e, o);
  }
  return (
    (r.displayName = "Memo(" + (e.displayName || e.name) + ")"),
    (r.prototype.isReactComponent = !0),
    (r.__f = !0),
    r
  );
}
((xt.prototype = new W()).isPureReactComponent = !0),
  (xt.prototype.shouldComponentUpdate = function (e, n) {
    return Rt(this.props, e) || Rt(this.state, n);
  });
var zn = h.__b;
h.__b = function (e) {
  e.type && e.type.__f && e.ref && ((e.props.ref = e.ref), (e.ref = null)),
    zn && zn(e);
};
var Vo =
  (typeof Symbol < "u" && Symbol.for && Symbol.for("react.forward_ref")) ||
  3911;
function Io(e) {
  function n(t) {
    var r = Xn({}, t);
    return delete r.ref, e(r, t.ref || null);
  }
  return (
    (n.$$typeof = Vo),
    (n.render = n),
    (n.prototype.isReactComponent = n.__f = !0),
    (n.displayName = "ForwardRef(" + (e.displayName || e.name) + ")"),
    n
  );
}
var Gn = function (e, n) {
    return e == null ? null : ne(ne(e).map(n));
  },
  To = {
    map: Gn,
    forEach: Gn,
    count: function (e) {
      return e ? ne(e).length : 0;
    },
    only: function (e) {
      var n = ne(e);
      if (n.length !== 1) throw "Children.only";
      return n[0];
    },
    toArray: ne,
  },
  Do = h.__e;
h.__e = function (e, n, t, r) {
  if (e.then) {
    for (var o, i = n; (i = i.__); )
      if ((o = i.__c) && o.__c)
        return n.__e == null && ((n.__e = t.__e), (n.__k = t.__k)), o.__c(e, n);
  }
  Do(e, n, t, r);
};
var Bn = h.unmount;
function Yn(e, n, t) {
  return (
    e &&
      (e.__c &&
        e.__c.__H &&
        (e.__c.__H.__.forEach(function (r) {
          typeof r.__c == "function" && r.__c();
        }),
        (e.__c.__H = null)),
      (e = Xn({}, e)).__c != null &&
        (e.__c.__P === t && (e.__c.__P = n), (e.__c = null)),
      (e.__k =
        e.__k &&
        e.__k.map(function (r) {
          return Yn(r, n, t);
        }))),
    e
  );
}
function Jn(e, n, t) {
  return (
    e &&
      ((e.__v = null),
      (e.__k =
        e.__k &&
        e.__k.map(function (r) {
          return Jn(r, n, t);
        })),
      e.__c &&
        e.__c.__P === n &&
        (e.__e && t.insertBefore(e.__e, e.__d),
        (e.__c.__e = !0),
        (e.__c.__P = t))),
    e
  );
}
function Ye() {
  (this.__u = 0), (this.t = null), (this.__b = null);
}
function Qn(e) {
  var n = e.__.__c;
  return n && n.__a && n.__a(e);
}
function Oo(e) {
  var n, t, r;
  function o(i) {
    if (
      (n ||
        (n = e()).then(
          function (l) {
            t = l.default || l;
          },
          function (l) {
            r = l;
          }
        ),
      r)
    )
      throw r;
    if (!t) throw n;
    return G(t, i);
  }
  return (o.displayName = "Lazy"), (o.__f = !0), o;
}
function Ne() {
  (this.u = null), (this.o = null);
}
(h.unmount = function (e) {
  var n = e.__c;
  n && n.__R && n.__R(), n && e.__h === !0 && (e.type = null), Bn && Bn(e);
}),
  ((Ye.prototype = new W()).__c = function (e, n) {
    var t = n.__c,
      r = this;
    r.t == null && (r.t = []), r.t.push(t);
    var o = Qn(r.__v),
      i = !1,
      l = function () {
        i || ((i = !0), (t.__R = null), o ? o(u) : u());
      };
    t.__R = l;
    var u = function () {
        if (!--r.__u) {
          if (r.state.__a) {
            var d = r.state.__a;
            r.__v.__k[0] = Jn(d, d.__c.__P, d.__c.__O);
          }
          var s;
          for (r.setState({ __a: (r.__b = null) }); (s = r.t.pop()); )
            s.forceUpdate();
        }
      },
      a = n.__h === !0;
    r.__u++ || a || r.setState({ __a: (r.__b = r.__v.__k[0]) }), e.then(l, l);
  }),
  (Ye.prototype.componentWillUnmount = function () {
    this.t = [];
  }),
  (Ye.prototype.render = function (e, n) {
    if (this.__b) {
      if (this.__v.__k) {
        var t = document.createElement("div"),
          r = this.__v.__k[0].__c;
        this.__v.__k[0] = Yn(this.__b, t, (r.__O = r.__P));
      }
      this.__b = null;
    }
    var o = n.__a && G(te, null, e.fallback);
    return o && (o.__h = null), [G(te, null, n.__a ? null : e.children), o];
  });
var Un = function (e, n, t) {
  if (
    (++t[1] === t[0] && e.o.delete(n),
    e.props.revealOrder && (e.props.revealOrder[0] !== "t" || !e.o.size))
  )
    for (t = e.u; t; ) {
      for (; t.length > 3; ) t.pop()();
      if (t[1] < t[0]) break;
      e.u = t = t[2];
    }
};
function Ao(e) {
  return (
    (this.getChildContext = function () {
      return e.context;
    }),
    e.children
  );
}
function No(e) {
  var n = this,
    t = e.i;
  (n.componentWillUnmount = function () {
    Ce(null, n.l), (n.l = null), (n.i = null);
  }),
    n.i && n.i !== t && n.componentWillUnmount(),
    e.__v
      ? (n.l ||
          ((n.i = t),
          (n.l = {
            nodeType: 1,
            parentNode: t,
            childNodes: [],
            appendChild: function (r) {
              this.childNodes.push(r), n.i.appendChild(r);
            },
            insertBefore: function (r, o) {
              this.childNodes.push(r), n.i.appendChild(r);
            },
            removeChild: function (r) {
              this.childNodes.splice(this.childNodes.indexOf(r) >>> 1, 1),
                n.i.removeChild(r);
            },
          })),
        Ce(G(Ao, { context: n.context }, e.__v), n.l))
      : n.l && n.componentWillUnmount();
}
function Po(e, n) {
  var t = G(No, { __v: e, i: n });
  return (t.containerInfo = n), t;
}
((Ne.prototype = new W()).__a = function (e) {
  var n = this,
    t = Qn(n.__v),
    r = n.o.get(e);
  return (
    r[0]++,
    function (o) {
      var i = function () {
        n.props.revealOrder ? (r.push(o), Un(n, e, r)) : o();
      };
      t ? t(i) : i();
    }
  );
}),
  (Ne.prototype.render = function (e) {
    (this.u = null), (this.o = new Map());
    var n = ne(e.children);
    e.revealOrder && e.revealOrder[0] === "b" && n.reverse();
    for (var t = n.length; t--; ) this.o.set(n[t], (this.u = [1, 0, this.u]));
    return e.children;
  }),
  (Ne.prototype.componentDidUpdate = Ne.prototype.componentDidMount =
    function () {
      var e = this;
      this.o.forEach(function (n, t) {
        Un(e, t, n);
      });
    });
var Zn =
    (typeof Symbol < "u" && Symbol.for && Symbol.for("react.element")) || 60103,
  ko =
    /^(?:accent|alignment|arabic|baseline|cap|clip(?!PathU)|color|dominant|fill|flood|font|glyph(?!R)|horiz|image(!S)|letter|lighting|marker(?!H|W|U)|overline|paint|pointer|shape|stop|strikethrough|stroke|text(?!L)|transform|underline|unicode|units|v|vector|vert|word|writing|x(?!C))[A-Z]/,
  Ho = /^on(Ani|Tra|Tou|BeforeInp|Compo)/,
  Lo = /[A-Z0-9]/g,
  zo = typeof document < "u",
  Go = function (e) {
    return (
      typeof Symbol < "u" && typeof Symbol() == "symbol"
        ? /fil|che|rad/
        : /fil|che|ra/
    ).test(e);
  };
function Ft(e, n, t) {
  return (
    n.__k == null && (n.textContent = ""),
    Ce(e, n),
    typeof t == "function" && t(),
    e ? e.__c : null
  );
}
function er(e, n, t) {
  return yt(e, n), typeof t == "function" && t(), e ? e.__c : null;
}
(W.prototype.isReactComponent = {}),
  [
    "componentWillMount",
    "componentWillReceiveProps",
    "componentWillUpdate",
  ].forEach(function (e) {
    Object.defineProperty(W.prototype, e, {
      configurable: !0,
      get: function () {
        return this["UNSAFE_" + e];
      },
      set: function (n) {
        Object.defineProperty(this, e, {
          configurable: !0,
          writable: !0,
          value: n,
        });
      },
    });
  });
var jn = h.event;
function Bo() {}
function Uo() {
  return this.cancelBubble;
}
function jo() {
  return this.defaultPrevented;
}
h.event = function (e) {
  return (
    jn && (e = jn(e)),
    (e.persist = Bo),
    (e.isPropagationStopped = Uo),
    (e.isDefaultPrevented = jo),
    (e.nativeEvent = e)
  );
};
var Mt,
  Ko = {
    enumerable: !1,
    configurable: !0,
    get: function () {
      return this.class;
    },
  },
  Kn = h.vnode;
h.vnode = function (e) {
  typeof e.type == "string" &&
    (function (n) {
      var t = n.props,
        r = n.type,
        o = {};
      for (var i in t) {
        var l = t[i];
        if (
          !(
            (i === "value" && "defaultValue" in t && l == null) ||
            (zo && i === "children" && r === "noscript") ||
            i === "class" ||
            i === "className"
          )
        ) {
          var u = i.toLowerCase();
          i === "defaultValue" && "value" in t && t.value == null
            ? (i = "value")
            : i === "download" && l === !0
            ? (l = "")
            : u === "ondoubleclick"
            ? (i = "ondblclick")
            : u !== "onchange" ||
              (r !== "input" && r !== "textarea") ||
              Go(t.type)
            ? u === "onfocus"
              ? (i = "onfocusin")
              : u === "onblur"
              ? (i = "onfocusout")
              : Ho.test(i)
              ? (i = u)
              : r.indexOf("-") === -1 && ko.test(i)
              ? (i = i.replace(Lo, "-$&").toLowerCase())
              : l === null && (l = void 0)
            : (u = i = "oninput"),
            u === "oninput" && o[(i = u)] && (i = "oninputCapture"),
            (o[i] = l);
        }
      }
      r == "select" &&
        o.multiple &&
        Array.isArray(o.value) &&
        (o.value = ne(t.children).forEach(function (a) {
          a.props.selected = o.value.indexOf(a.props.value) != -1;
        })),
        r == "select" &&
          o.defaultValue != null &&
          (o.value = ne(t.children).forEach(function (a) {
            a.props.selected = o.multiple
              ? o.defaultValue.indexOf(a.props.value) != -1
              : o.defaultValue == a.props.value;
          })),
        t.class && !t.className
          ? ((o.class = t.class), Object.defineProperty(o, "className", Ko))
          : ((t.className && !t.class) || (t.class && t.className)) &&
            (o.class = o.className = t.className),
        (n.props = o);
    })(e),
    (e.$$typeof = Zn),
    Kn && Kn(e);
};
var qn = h.__r;
h.__r = function (e) {
  qn && qn(e), (Mt = e.__c);
};
var Wn = h.diffed;
h.diffed = function (e) {
  Wn && Wn(e);
  var n = e.props,
    t = e.__e;
  t != null &&
    e.type === "textarea" &&
    "value" in n &&
    n.value !== t.value &&
    (t.value = n.value == null ? "" : n.value),
    (Mt = null);
};
var qo = {
  ReactCurrentDispatcher: {
    current: {
      readContext: function (e) {
        return Mt.__n[e.__c].props.value;
      },
    },
  },
};
function Wo(e) {
  return G.bind(null, e);
}
function tr(e) {
  return !!e && e.$$typeof === Zn;
}
function Xo(e) {
  return tr(e) ? Fn.apply(null, arguments) : e;
}
function $t(e) {
  return !!e.__k && (Ce(null, e), !0);
}
function Yo(e) {
  return (e && (e.base || (e.nodeType === 1 && e))) || null;
}
var Jo = function (e, n) {
    return e(n);
  },
  Qo = function (e, n) {
    return e(n);
  },
  Vt = te;
function nr(e) {
  e();
}
function Zo(e) {
  return e;
}
function ei() {
  return [!1, nr];
}
var ti = re;
function ni(e, n) {
  var t = n(),
    r = D({ h: { __: t, v: n } }),
    o = r[0].h,
    i = r[1];
  return (
    re(
      function () {
        (o.__ = t), (o.v = n), Et(o.__, n()) || i({ h: o });
      },
      [e, t, n]
    ),
    L(
      function () {
        return (
          Et(o.__, o.v()) || i({ h: o }),
          e(function () {
            Et(o.__, o.v()) || i({ h: o });
          })
        );
      },
      [e]
    ),
    t
  );
}
var b = {
  useState: D,
  useId: Hn,
  useReducer: xe,
  useEffect: L,
  useLayoutEffect: re,
  useInsertionEffect: ti,
  useTransition: ei,
  useDeferredValue: Zo,
  useSyncExternalStore: ni,
  startTransition: nr,
  useRef: B,
  useImperativeHandle: Nn,
  useMemo: oe,
  useCallback: se,
  useContext: Pn,
  useDebugValue: kn,
  version: "17.0.2",
  Children: To,
  render: Ft,
  hydrate: er,
  unmountComponentAtNode: $t,
  createPortal: Po,
  createElement: G,
  createContext: bt,
  createFactory: Wo,
  cloneElement: Xo,
  createRef: ht,
  Fragment: te,
  isValidElement: tr,
  findDOMNode: Yo,
  Component: W,
  PureComponent: xt,
  memo: $o,
  forwardRef: Io,
  flushSync: Qo,
  unstable_batchedUpdates: Jo,
  StrictMode: Vt,
  Suspense: Ye,
  SuspenseList: Ne,
  lazy: Oo,
  __SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED: qo,
};
function pe(e, n) {
  return typeof e == "function" ? e(n) : e;
}
function X(e, n) {
  return (t) => {
    n.setState((r) => ({ ...r, [e]: pe(t, r[e]) }));
  };
}
function et(e) {
  return e instanceof Function;
}
function ri(e) {
  return Array.isArray(e) && e.every((n) => typeof n == "number");
}
function oi(e, n) {
  let t = [],
    r = (o) => {
      o.forEach((i) => {
        t.push(i);
        let l = n(i);
        l != null && l.length && r(l);
      });
    };
  return r(e), t;
}
function y(e, n, t) {
  let r = [],
    o;
  return () => {
    let i;
    t.key && t.debug && (i = Date.now());
    let l = e();
    if (!(l.length !== r.length || l.some((d, s) => r[s] !== d))) return o;
    r = l;
    let a;
    if (
      (t.key && t.debug && (a = Date.now()),
      (o = n(...l)),
      t == null || t.onChange == null || t.onChange(o),
      t.key && t.debug && t != null && t.debug())
    ) {
      let d = Math.round((Date.now() - i) * 100) / 100,
        s = Math.round((Date.now() - a) * 100) / 100,
        g = s / 16,
        f = (c, p) => {
          for (c = String(c); c.length < p; ) c = " " + c;
          return c;
        };
      console.info(
        `%c\u23F1 ${f(s, 5)} /${f(d, 5)} ms`,
        `
            font-size: .6rem;
            font-weight: bold;
            color: hsl(${Math.max(
              0,
              Math.min(120 - 120 * g, 120)
            )}deg 100% 31%);`,
        t?.key
      );
    }
    return o;
  };
}
function ii(e, n, t, r) {
  var o, i;
  let u = { ...e._getDefaultColumnDef(), ...n },
    a = u.accessorKey,
    d =
      (o = (i = u.id) != null ? i : a ? a.replace(".", "_") : void 0) != null
        ? o
        : typeof u.header == "string"
        ? u.header
        : void 0,
    s;
  if (
    (u.accessorFn
      ? (s = u.accessorFn)
      : a &&
        (a.includes(".")
          ? (s = (f) => {
              let c = f;
              for (let m of a.split(".")) {
                var p;
                c = (p = c) == null ? void 0 : p[m];
              }
              return c;
            })
          : (s = (f) => f[u.accessorKey])),
    !d)
  )
    throw new Error();
  let g = {
    id: `${String(d)}`,
    accessorFn: s,
    parent: r,
    depth: t,
    columnDef: u,
    columns: [],
    getFlatColumns: y(
      () => [!0],
      () => {
        var f;
        return [
          g,
          ...((f = g.columns) == null
            ? void 0
            : f.flatMap((c) => c.getFlatColumns())),
        ];
      },
      {
        key: "column.getFlatColumns",
        debug: () => {
          var f;
          return (f = e.options.debugAll) != null ? f : e.options.debugColumns;
        },
      }
    ),
    getLeafColumns: y(
      () => [e._getOrderColumnsFn()],
      (f) => {
        var c;
        if ((c = g.columns) != null && c.length) {
          let p = g.columns.flatMap((m) => m.getLeafColumns());
          return f(p);
        }
        return [g];
      },
      {
        key: "column.getLeafColumns",
        debug: () => {
          var f;
          return (f = e.options.debugAll) != null ? f : e.options.debugColumns;
        },
      }
    ),
  };
  return (
    (g = e._features.reduce(
      (f, c) =>
        Object.assign(
          f,
          c.createColumn == null ? void 0 : c.createColumn(g, e)
        ),
      g
    )),
    g
  );
}
function or(e, n, t) {
  var r;
  let i = {
    id: (r = t.id) != null ? r : n.id,
    column: n,
    index: t.index,
    isPlaceholder: !!t.isPlaceholder,
    placeholderId: t.placeholderId,
    depth: t.depth,
    subHeaders: [],
    colSpan: 0,
    rowSpan: 0,
    headerGroup: null,
    getLeafHeaders: () => {
      let l = [],
        u = (a) => {
          a.subHeaders && a.subHeaders.length && a.subHeaders.map(u), l.push(a);
        };
      return u(i), l;
    },
    getContext: () => ({ table: e, header: i, column: n }),
  };
  return (
    e._features.forEach((l) => {
      Object.assign(i, l.createHeader == null ? void 0 : l.createHeader(i, e));
    }),
    i
  );
}
var li = {
  createTable: (e) => ({
    getHeaderGroups: y(
      () => [
        e.getAllColumns(),
        e.getVisibleLeafColumns(),
        e.getState().columnPinning.left,
        e.getState().columnPinning.right,
      ],
      (n, t, r, o) => {
        var i, l;
        let u =
            (i = r?.map((g) => t.find((f) => f.id === g)).filter(Boolean)) !=
            null
              ? i
              : [],
          a =
            (l = o?.map((g) => t.find((f) => f.id === g)).filter(Boolean)) !=
            null
              ? l
              : [],
          d = t.filter(
            (g) =>
              !(r != null && r.includes(g.id)) &&
              !(o != null && o.includes(g.id))
          );
        return Je(n, [...u, ...d, ...a], e);
      },
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getCenterHeaderGroups: y(
      () => [
        e.getAllColumns(),
        e.getVisibleLeafColumns(),
        e.getState().columnPinning.left,
        e.getState().columnPinning.right,
      ],
      (n, t, r, o) => (
        (t = t.filter(
          (i) =>
            !(r != null && r.includes(i.id)) && !(o != null && o.includes(i.id))
        )),
        Je(n, t, e, "center")
      ),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getLeftHeaderGroups: y(
      () => [
        e.getAllColumns(),
        e.getVisibleLeafColumns(),
        e.getState().columnPinning.left,
      ],
      (n, t, r) => {
        var o;
        let i =
          (o = r?.map((l) => t.find((u) => u.id === l)).filter(Boolean)) != null
            ? o
            : [];
        return Je(n, i, e, "left");
      },
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getRightHeaderGroups: y(
      () => [
        e.getAllColumns(),
        e.getVisibleLeafColumns(),
        e.getState().columnPinning.right,
      ],
      (n, t, r) => {
        var o;
        let i =
          (o = r?.map((l) => t.find((u) => u.id === l)).filter(Boolean)) != null
            ? o
            : [];
        return Je(n, i, e, "right");
      },
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getFooterGroups: y(
      () => [e.getHeaderGroups()],
      (n) => [...n].reverse(),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getLeftFooterGroups: y(
      () => [e.getLeftHeaderGroups()],
      (n) => [...n].reverse(),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getCenterFooterGroups: y(
      () => [e.getCenterHeaderGroups()],
      (n) => [...n].reverse(),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getRightFooterGroups: y(
      () => [e.getRightHeaderGroups()],
      (n) => [...n].reverse(),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getFlatHeaders: y(
      () => [e.getHeaderGroups()],
      (n) => n.map((t) => t.headers).flat(),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getLeftFlatHeaders: y(
      () => [e.getLeftHeaderGroups()],
      (n) => n.map((t) => t.headers).flat(),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getCenterFlatHeaders: y(
      () => [e.getCenterHeaderGroups()],
      (n) => n.map((t) => t.headers).flat(),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getRightFlatHeaders: y(
      () => [e.getRightHeaderGroups()],
      (n) => n.map((t) => t.headers).flat(),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getCenterLeafHeaders: y(
      () => [e.getCenterFlatHeaders()],
      (n) =>
        n.filter((t) => {
          var r;
          return !((r = t.subHeaders) != null && r.length);
        }),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getLeftLeafHeaders: y(
      () => [e.getLeftFlatHeaders()],
      (n) =>
        n.filter((t) => {
          var r;
          return !((r = t.subHeaders) != null && r.length);
        }),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getRightLeafHeaders: y(
      () => [e.getRightFlatHeaders()],
      (n) =>
        n.filter((t) => {
          var r;
          return !((r = t.subHeaders) != null && r.length);
        }),
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
    getLeafHeaders: y(
      () => [
        e.getLeftHeaderGroups(),
        e.getCenterHeaderGroups(),
        e.getRightHeaderGroups(),
      ],
      (n, t, r) => {
        var o, i, l, u, a, d;
        return [
          ...((o = (i = n[0]) == null ? void 0 : i.headers) != null ? o : []),
          ...((l = (u = t[0]) == null ? void 0 : u.headers) != null ? l : []),
          ...((a = (d = r[0]) == null ? void 0 : d.headers) != null ? a : []),
        ]
          .map((s) => s.getLeafHeaders())
          .flat();
      },
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugHeaders;
        },
      }
    ),
  }),
};
function Je(e, n, t, r) {
  var o, i;
  let l = 0,
    u = function (f, c) {
      c === void 0 && (c = 1),
        (l = Math.max(l, c)),
        f
          .filter((p) => p.getIsVisible())
          .forEach((p) => {
            var m;
            (m = p.columns) != null && m.length && u(p.columns, c + 1);
          }, 0);
    };
  u(e);
  let a = [],
    d = (f, c) => {
      let p = {
          depth: c,
          id: [r, `${c}`].filter(Boolean).join("_"),
          headers: [],
        },
        m = [];
      f.forEach((_) => {
        let v = [...m].reverse()[0],
          w = _.column.depth === p.depth,
          x,
          M = !1;
        if (
          (w && _.column.parent
            ? (x = _.column.parent)
            : ((x = _.column), (M = !0)),
          v && v?.column === x)
        )
          v.subHeaders.push(_);
        else {
          let I = or(t, x, {
            id: [r, c, x.id, _?.id].filter(Boolean).join("_"),
            isPlaceholder: M,
            placeholderId: M
              ? `${m.filter((N) => N.column === x).length}`
              : void 0,
            depth: c,
            index: m.length,
          });
          I.subHeaders.push(_), m.push(I);
        }
        p.headers.push(_), (_.headerGroup = p);
      }),
        a.push(p),
        c > 0 && d(m, c - 1);
    },
    s = n.map((f, c) => or(t, f, { depth: l, index: c }));
  d(s, l - 1), a.reverse();
  let g = (f) =>
    f
      .filter((p) => p.column.getIsVisible())
      .map((p) => {
        let m = 0,
          _ = 0,
          v = [0];
        p.subHeaders && p.subHeaders.length
          ? ((v = []),
            g(p.subHeaders).forEach((x) => {
              let { colSpan: M, rowSpan: I } = x;
              (m += M), v.push(I);
            }))
          : (m = 1);
        let w = Math.min(...v);
        return (
          (_ = _ + w),
          (p.colSpan = m),
          (p.rowSpan = _),
          { colSpan: m, rowSpan: _ }
        );
      });
  return g((o = (i = a[0]) == null ? void 0 : i.headers) != null ? o : []), a;
}
var Qe = { size: 150, minSize: 20, maxSize: Number.MAX_SAFE_INTEGER },
  It = () => ({
    startOffset: null,
    startSize: null,
    deltaOffset: null,
    deltaPercentage: null,
    isResizingColumn: !1,
    columnSizingStart: [],
  }),
  si = {
    getDefaultColumnDef: () => Qe,
    getInitialState: (e) => ({
      columnSizing: {},
      columnSizingInfo: It(),
      ...e,
    }),
    getDefaultOptions: (e) => ({
      columnResizeMode: "onEnd",
      onColumnSizingChange: X("columnSizing", e),
      onColumnSizingInfoChange: X("columnSizingInfo", e),
    }),
    createColumn: (e, n) => ({
      getSize: () => {
        var t, r, o;
        let i = n.getState().columnSizing[e.id];
        return Math.min(
          Math.max(
            (t = e.columnDef.minSize) != null ? t : Qe.minSize,
            (r = i ?? e.columnDef.size) != null ? r : Qe.size
          ),
          (o = e.columnDef.maxSize) != null ? o : Qe.maxSize
        );
      },
      getStart: (t) => {
        let r = t
            ? t === "left"
              ? n.getLeftVisibleLeafColumns()
              : n.getRightVisibleLeafColumns()
            : n.getVisibleLeafColumns(),
          o = r.findIndex((i) => i.id === e.id);
        if (o > 0) {
          let i = r[o - 1];
          return i.getStart(t) + i.getSize();
        }
        return 0;
      },
      resetSize: () => {
        n.setColumnSizing((t) => {
          let { [e.id]: r, ...o } = t;
          return o;
        });
      },
      getCanResize: () => {
        var t, r;
        return (
          ((t = e.columnDef.enableResizing) != null ? t : !0) &&
          ((r = n.options.enableColumnResizing) != null ? r : !0)
        );
      },
      getIsResizing: () =>
        n.getState().columnSizingInfo.isResizingColumn === e.id,
    }),
    createHeader: (e, n) => ({
      getSize: () => {
        let t = 0,
          r = (o) => {
            if (o.subHeaders.length) o.subHeaders.forEach(r);
            else {
              var i;
              t += (i = o.column.getSize()) != null ? i : 0;
            }
          };
        return r(e), t;
      },
      getStart: () => {
        if (e.index > 0) {
          let t = e.headerGroup.headers[e.index - 1];
          return t.getStart() + t.getSize();
        }
        return 0;
      },
      getResizeHandler: () => {
        let t = n.getColumn(e.column.id),
          r = t?.getCanResize();
        return (o) => {
          if (
            !t ||
            !r ||
            (o.persist == null || o.persist(),
            Tt(o) && o.touches && o.touches.length > 1)
          )
            return;
          let i = e.getSize(),
            l = e
              ? e.getLeafHeaders().map((m) => [m.column.id, m.column.getSize()])
              : [[t.id, t.getSize()]],
            u = Tt(o) ? Math.round(o.touches[0].clientX) : o.clientX,
            a = {},
            d = (m, _) => {
              typeof _ == "number" &&
                (n.setColumnSizingInfo((v) => {
                  var w, x;
                  let M = _ - ((w = v?.startOffset) != null ? w : 0),
                    I = Math.max(
                      M / ((x = v?.startSize) != null ? x : 0),
                      -0.999999
                    );
                  return (
                    v.columnSizingStart.forEach((N) => {
                      let [J, O] = N;
                      a[J] = Math.round(Math.max(O + O * I, 0) * 100) / 100;
                    }),
                    { ...v, deltaOffset: M, deltaPercentage: I }
                  );
                }),
                (n.options.columnResizeMode === "onChange" || m === "end") &&
                  n.setColumnSizing((v) => ({ ...v, ...a })));
            },
            s = (m) => d("move", m),
            g = (m) => {
              d("end", m),
                n.setColumnSizingInfo((_) => ({
                  ..._,
                  isResizingColumn: !1,
                  startOffset: null,
                  startSize: null,
                  deltaOffset: null,
                  deltaPercentage: null,
                  columnSizingStart: [],
                }));
            },
            f = {
              moveHandler: (m) => s(m.clientX),
              upHandler: (m) => {
                document.removeEventListener("mousemove", f.moveHandler),
                  document.removeEventListener("mouseup", f.upHandler),
                  g(m.clientX);
              },
            },
            c = {
              moveHandler: (m) => (
                m.cancelable && (m.preventDefault(), m.stopPropagation()),
                s(m.touches[0].clientX),
                !1
              ),
              upHandler: (m) => {
                var _;
                document.removeEventListener("touchmove", c.moveHandler),
                  document.removeEventListener("touchend", c.upHandler),
                  m.cancelable && (m.preventDefault(), m.stopPropagation()),
                  g((_ = m.touches[0]) == null ? void 0 : _.clientX);
              },
            },
            p = ai() ? { passive: !1 } : !1;
          Tt(o)
            ? (document.addEventListener("touchmove", c.moveHandler, p),
              document.addEventListener("touchend", c.upHandler, p))
            : (document.addEventListener("mousemove", f.moveHandler, p),
              document.addEventListener("mouseup", f.upHandler, p)),
            n.setColumnSizingInfo((m) => ({
              ...m,
              startOffset: u,
              startSize: i,
              deltaOffset: 0,
              deltaPercentage: 0,
              columnSizingStart: l,
              isResizingColumn: t.id,
            }));
        };
      },
    }),
    createTable: (e) => ({
      setColumnSizing: (n) =>
        e.options.onColumnSizingChange == null
          ? void 0
          : e.options.onColumnSizingChange(n),
      setColumnSizingInfo: (n) =>
        e.options.onColumnSizingInfoChange == null
          ? void 0
          : e.options.onColumnSizingInfoChange(n),
      resetColumnSizing: (n) => {
        var t;
        e.setColumnSizing(
          n ? {} : (t = e.initialState.columnSizing) != null ? t : {}
        );
      },
      resetHeaderSizeInfo: (n) => {
        var t;
        e.setColumnSizingInfo(
          n ? It() : (t = e.initialState.columnSizingInfo) != null ? t : It()
        );
      },
      getTotalSize: () => {
        var n, t;
        return (n =
          (t = e.getHeaderGroups()[0]) == null
            ? void 0
            : t.headers.reduce((r, o) => r + o.getSize(), 0)) != null
          ? n
          : 0;
      },
      getLeftTotalSize: () => {
        var n, t;
        return (n =
          (t = e.getLeftHeaderGroups()[0]) == null
            ? void 0
            : t.headers.reduce((r, o) => r + o.getSize(), 0)) != null
          ? n
          : 0;
      },
      getCenterTotalSize: () => {
        var n, t;
        return (n =
          (t = e.getCenterHeaderGroups()[0]) == null
            ? void 0
            : t.headers.reduce((r, o) => r + o.getSize(), 0)) != null
          ? n
          : 0;
      },
      getRightTotalSize: () => {
        var n, t;
        return (n =
          (t = e.getRightHeaderGroups()[0]) == null
            ? void 0
            : t.headers.reduce((r, o) => r + o.getSize(), 0)) != null
          ? n
          : 0;
      },
    }),
  },
  Ze = null;
function ai() {
  if (typeof Ze == "boolean") return Ze;
  let e = !1;
  try {
    let n = {
        get passive() {
          return (e = !0), !1;
        },
      },
      t = () => {};
    window.addEventListener("test", t, n),
      window.removeEventListener("test", t);
  } catch {
    e = !1;
  }
  return (Ze = e), Ze;
}
function Tt(e) {
  return e.type === "touchstart";
}
var ui = {
    getInitialState: (e) => ({ expanded: {}, ...e }),
    getDefaultOptions: (e) => ({
      onExpandedChange: X("expanded", e),
      paginateExpandedRows: !0,
    }),
    createTable: (e) => {
      let n = !1,
        t = !1;
      return {
        _autoResetExpanded: () => {
          var r, o;
          if (!n) {
            e._queue(() => {
              n = !0;
            });
            return;
          }
          if (
            (r =
              (o = e.options.autoResetAll) != null
                ? o
                : e.options.autoResetExpanded) != null
              ? r
              : !e.options.manualExpanding
          ) {
            if (t) return;
            (t = !0),
              e._queue(() => {
                e.resetExpanded(), (t = !1);
              });
          }
        },
        setExpanded: (r) =>
          e.options.onExpandedChange == null
            ? void 0
            : e.options.onExpandedChange(r),
        toggleAllRowsExpanded: (r) => {
          r ?? !e.getIsAllRowsExpanded()
            ? e.setExpanded(!0)
            : e.setExpanded({});
        },
        resetExpanded: (r) => {
          var o, i;
          e.setExpanded(
            r
              ? {}
              : (o = (i = e.initialState) == null ? void 0 : i.expanded) != null
              ? o
              : {}
          );
        },
        getCanSomeRowsExpand: () =>
          e.getPrePaginationRowModel().flatRows.some((r) => r.getCanExpand()),
        getToggleAllRowsExpandedHandler: () => (r) => {
          r.persist == null || r.persist(), e.toggleAllRowsExpanded();
        },
        getIsSomeRowsExpanded: () => {
          let r = e.getState().expanded;
          return r === !0 || Object.values(r).some(Boolean);
        },
        getIsAllRowsExpanded: () => {
          let r = e.getState().expanded;
          return typeof r == "boolean"
            ? r === !0
            : !(
                !Object.keys(r).length ||
                e.getRowModel().flatRows.some((o) => !o.getIsExpanded())
              );
        },
        getExpandedDepth: () => {
          let r = 0;
          return (
            (e.getState().expanded === !0
              ? Object.keys(e.getRowModel().rowsById)
              : Object.keys(e.getState().expanded)
            ).forEach((i) => {
              let l = i.split(".");
              r = Math.max(r, l.length);
            }),
            r
          );
        },
        getPreExpandedRowModel: () => e.getSortedRowModel(),
        getExpandedRowModel: () => (
          !e._getExpandedRowModel &&
            e.options.getExpandedRowModel &&
            (e._getExpandedRowModel = e.options.getExpandedRowModel(e)),
          e.options.manualExpanding || !e._getExpandedRowModel
            ? e.getPreExpandedRowModel()
            : e._getExpandedRowModel()
        ),
      };
    },
    createRow: (e, n) => ({
      toggleExpanded: (t) => {
        n.setExpanded((r) => {
          var o;
          let i = r === !0 ? !0 : !!(r != null && r[e.id]),
            l = {};
          if (
            (r === !0
              ? Object.keys(n.getRowModel().rowsById).forEach((u) => {
                  l[u] = !0;
                })
              : (l = r),
            (t = (o = t) != null ? o : !i),
            !i && t)
          )
            return { ...l, [e.id]: !0 };
          if (i && !t) {
            let { [e.id]: u, ...a } = l;
            return a;
          }
          return r;
        });
      },
      getIsExpanded: () => {
        var t;
        let r = n.getState().expanded;
        return !!((t =
          n.options.getIsRowExpanded == null
            ? void 0
            : n.options.getIsRowExpanded(e)) != null
          ? t
          : r === !0 || r?.[e.id]);
      },
      getCanExpand: () => {
        var t, r, o;
        return (t =
          n.options.getRowCanExpand == null
            ? void 0
            : n.options.getRowCanExpand(e)) != null
          ? t
          : ((r = n.options.enableExpanding) != null ? r : !0) &&
              !!((o = e.subRows) != null && o.length);
      },
      getToggleExpandedHandler: () => {
        let t = e.getCanExpand();
        return () => {
          t && e.toggleExpanded();
        };
      },
    }),
  },
  ar = (e, n, t) => {
    var r, o, i;
    let l = t.toLowerCase();
    return !!(
      !(
        (r = e.getValue(n)) == null ||
        (o = r.toString()) == null ||
        (i = o.toLowerCase()) == null
      ) && i.includes(l)
    );
  };
ar.autoRemove = (e) => Z(e);
var ur = (e, n, t) => {
  var r, o;
  return !!(
    !((r = e.getValue(n)) == null || (o = r.toString()) == null) &&
    o.includes(t)
  );
};
ur.autoRemove = (e) => Z(e);
var dr = (e, n, t) => {
  var r, o;
  return (
    ((r = e.getValue(n)) == null || (o = r.toString()) == null
      ? void 0
      : o.toLowerCase()) === t?.toLowerCase()
  );
};
dr.autoRemove = (e) => Z(e);
var cr = (e, n, t) => {
  var r;
  return (r = e.getValue(n)) == null ? void 0 : r.includes(t);
};
cr.autoRemove = (e) => Z(e) || !(e != null && e.length);
var fr = (e, n, t) =>
  !t.some((r) => {
    var o;
    return !((o = e.getValue(n)) != null && o.includes(r));
  });
fr.autoRemove = (e) => Z(e) || !(e != null && e.length);
var gr = (e, n, t) =>
  t.some((r) => {
    var o;
    return (o = e.getValue(n)) == null ? void 0 : o.includes(r);
  });
gr.autoRemove = (e) => Z(e) || !(e != null && e.length);
var pr = (e, n, t) => e.getValue(n) === t;
pr.autoRemove = (e) => Z(e);
var mr = (e, n, t) => e.getValue(n) == t;
mr.autoRemove = (e) => Z(e);
var zt = (e, n, t) => {
  let [r, o] = t,
    i = e.getValue(n);
  return i >= r && i <= o;
};
zt.resolveFilterValue = (e) => {
  let [n, t] = e,
    r = typeof n != "number" ? parseFloat(n) : n,
    o = typeof t != "number" ? parseFloat(t) : t,
    i = n === null || Number.isNaN(r) ? -1 / 0 : r,
    l = t === null || Number.isNaN(o) ? 1 / 0 : o;
  if (i > l) {
    let u = i;
    (i = l), (l = u);
  }
  return [i, l];
};
zt.autoRemove = (e) => Z(e) || (Z(e[0]) && Z(e[1]));
var ae = {
  includesString: ar,
  includesStringSensitive: ur,
  equalsString: dr,
  arrIncludes: cr,
  arrIncludesAll: fr,
  arrIncludesSome: gr,
  equals: pr,
  weakEquals: mr,
  inNumberRange: zt,
};
function Z(e) {
  return e == null || e === "";
}
var di = {
  getDefaultColumnDef: () => ({ filterFn: "auto" }),
  getInitialState: (e) => ({ columnFilters: [], globalFilter: void 0, ...e }),
  getDefaultOptions: (e) => ({
    onColumnFiltersChange: X("columnFilters", e),
    onGlobalFilterChange: X("globalFilter", e),
    filterFromLeafRows: !1,
    maxLeafRowFilterDepth: 100,
    globalFilterFn: "auto",
    getColumnCanGlobalFilter: (n) => {
      var t, r;
      let o =
        (t = e.getCoreRowModel().flatRows[0]) == null ||
        (r = t._getAllCellsByColumnId()[n.id]) == null
          ? void 0
          : r.getValue();
      return typeof o == "string" || typeof o == "number";
    },
  }),
  createColumn: (e, n) => ({
    getAutoFilterFn: () => {
      let t = n.getCoreRowModel().flatRows[0],
        r = t?.getValue(e.id);
      return typeof r == "string"
        ? ae.includesString
        : typeof r == "number"
        ? ae.inNumberRange
        : typeof r == "boolean" || (r !== null && typeof r == "object")
        ? ae.equals
        : Array.isArray(r)
        ? ae.arrIncludes
        : ae.weakEquals;
    },
    getFilterFn: () => {
      var t, r;
      return et(e.columnDef.filterFn)
        ? e.columnDef.filterFn
        : e.columnDef.filterFn === "auto"
        ? e.getAutoFilterFn()
        : (t =
            (r = n.options.filterFns) == null
              ? void 0
              : r[e.columnDef.filterFn]) != null
        ? t
        : ae[e.columnDef.filterFn];
    },
    getCanFilter: () => {
      var t, r, o;
      return (
        ((t = e.columnDef.enableColumnFilter) != null ? t : !0) &&
        ((r = n.options.enableColumnFilters) != null ? r : !0) &&
        ((o = n.options.enableFilters) != null ? o : !0) &&
        !!e.accessorFn
      );
    },
    getCanGlobalFilter: () => {
      var t, r, o, i;
      return (
        ((t = e.columnDef.enableGlobalFilter) != null ? t : !0) &&
        ((r = n.options.enableGlobalFilter) != null ? r : !0) &&
        ((o = n.options.enableFilters) != null ? o : !0) &&
        ((i =
          n.options.getColumnCanGlobalFilter == null
            ? void 0
            : n.options.getColumnCanGlobalFilter(e)) != null
          ? i
          : !0) &&
        !!e.accessorFn
      );
    },
    getIsFiltered: () => e.getFilterIndex() > -1,
    getFilterValue: () => {
      var t, r;
      return (t = n.getState().columnFilters) == null ||
        (r = t.find((o) => o.id === e.id)) == null
        ? void 0
        : r.value;
    },
    getFilterIndex: () => {
      var t, r;
      return (t =
        (r = n.getState().columnFilters) == null
          ? void 0
          : r.findIndex((o) => o.id === e.id)) != null
        ? t
        : -1;
    },
    setFilterValue: (t) => {
      n.setColumnFilters((r) => {
        let o = e.getFilterFn(),
          i = r?.find((s) => s.id === e.id),
          l = pe(t, i ? i.value : void 0);
        if (ir(o, l, e)) {
          var u;
          return (u = r?.filter((s) => s.id !== e.id)) != null ? u : [];
        }
        let a = { id: e.id, value: l };
        if (i) {
          var d;
          return (d = r?.map((s) => (s.id === e.id ? a : s))) != null ? d : [];
        }
        return r != null && r.length ? [...r, a] : [a];
      });
    },
    _getFacetedRowModel:
      n.options.getFacetedRowModel && n.options.getFacetedRowModel(n, e.id),
    getFacetedRowModel: () =>
      e._getFacetedRowModel
        ? e._getFacetedRowModel()
        : n.getPreFilteredRowModel(),
    _getFacetedUniqueValues:
      n.options.getFacetedUniqueValues &&
      n.options.getFacetedUniqueValues(n, e.id),
    getFacetedUniqueValues: () =>
      e._getFacetedUniqueValues ? e._getFacetedUniqueValues() : new Map(),
    _getFacetedMinMaxValues:
      n.options.getFacetedMinMaxValues &&
      n.options.getFacetedMinMaxValues(n, e.id),
    getFacetedMinMaxValues: () => {
      if (e._getFacetedMinMaxValues) return e._getFacetedMinMaxValues();
    },
  }),
  createRow: (e, n) => ({ columnFilters: {}, columnFiltersMeta: {} }),
  createTable: (e) => ({
    getGlobalAutoFilterFn: () => ae.includesString,
    getGlobalFilterFn: () => {
      var n, t;
      let { globalFilterFn: r } = e.options;
      return et(r)
        ? r
        : r === "auto"
        ? e.getGlobalAutoFilterFn()
        : (n = (t = e.options.filterFns) == null ? void 0 : t[r]) != null
        ? n
        : ae[r];
    },
    setColumnFilters: (n) => {
      let t = e.getAllLeafColumns(),
        r = (o) => {
          var i;
          return (i = pe(n, o)) == null
            ? void 0
            : i.filter((l) => {
                let u = t.find((a) => a.id === l.id);
                if (u) {
                  let a = u.getFilterFn();
                  if (ir(a, l.value, u)) return !1;
                }
                return !0;
              });
        };
      e.options.onColumnFiltersChange == null ||
        e.options.onColumnFiltersChange(r);
    },
    setGlobalFilter: (n) => {
      e.options.onGlobalFilterChange == null ||
        e.options.onGlobalFilterChange(n);
    },
    resetGlobalFilter: (n) => {
      e.setGlobalFilter(n ? void 0 : e.initialState.globalFilter);
    },
    resetColumnFilters: (n) => {
      var t, r;
      e.setColumnFilters(
        n
          ? []
          : (t = (r = e.initialState) == null ? void 0 : r.columnFilters) !=
            null
          ? t
          : []
      );
    },
    getPreFilteredRowModel: () => e.getCoreRowModel(),
    getFilteredRowModel: () => (
      !e._getFilteredRowModel &&
        e.options.getFilteredRowModel &&
        (e._getFilteredRowModel = e.options.getFilteredRowModel(e)),
      e.options.manualFiltering || !e._getFilteredRowModel
        ? e.getPreFilteredRowModel()
        : e._getFilteredRowModel()
    ),
    _getGlobalFacetedRowModel:
      e.options.getFacetedRowModel &&
      e.options.getFacetedRowModel(e, "__global__"),
    getGlobalFacetedRowModel: () =>
      e.options.manualFiltering || !e._getGlobalFacetedRowModel
        ? e.getPreFilteredRowModel()
        : e._getGlobalFacetedRowModel(),
    _getGlobalFacetedUniqueValues:
      e.options.getFacetedUniqueValues &&
      e.options.getFacetedUniqueValues(e, "__global__"),
    getGlobalFacetedUniqueValues: () =>
      e._getGlobalFacetedUniqueValues
        ? e._getGlobalFacetedUniqueValues()
        : new Map(),
    _getGlobalFacetedMinMaxValues:
      e.options.getFacetedMinMaxValues &&
      e.options.getFacetedMinMaxValues(e, "__global__"),
    getGlobalFacetedMinMaxValues: () => {
      if (e._getGlobalFacetedMinMaxValues)
        return e._getGlobalFacetedMinMaxValues();
    },
  }),
};
function ir(e, n, t) {
  return (
    (e && e.autoRemove ? e.autoRemove(n, t) : !1) ||
    typeof n > "u" ||
    (typeof n == "string" && !n)
  );
}
var ci = (e, n, t) =>
    t.reduce((r, o) => {
      let i = o.getValue(e);
      return r + (typeof i == "number" ? i : 0);
    }, 0),
  fi = (e, n, t) => {
    let r;
    return (
      t.forEach((o) => {
        let i = o.getValue(e);
        i != null && (r > i || (r === void 0 && i >= i)) && (r = i);
      }),
      r
    );
  },
  gi = (e, n, t) => {
    let r;
    return (
      t.forEach((o) => {
        let i = o.getValue(e);
        i != null && (r < i || (r === void 0 && i >= i)) && (r = i);
      }),
      r
    );
  },
  pi = (e, n, t) => {
    let r, o;
    return (
      t.forEach((i) => {
        let l = i.getValue(e);
        l != null &&
          (r === void 0
            ? l >= l && (r = o = l)
            : (r > l && (r = l), o < l && (o = l)));
      }),
      [r, o]
    );
  },
  mi = (e, n) => {
    let t = 0,
      r = 0;
    if (
      (n.forEach((o) => {
        let i = o.getValue(e);
        i != null && (i = +i) >= i && (++t, (r += i));
      }),
      t)
    )
      return r / t;
  },
  _i = (e, n) => {
    if (!n.length) return;
    let t = n.map((i) => i.getValue(e));
    if (!ri(t)) return;
    if (t.length === 1) return t[0];
    let r = Math.floor(t.length / 2),
      o = t.sort((i, l) => i - l);
    return t.length % 2 !== 0 ? o[r] : (o[r - 1] + o[r]) / 2;
  },
  hi = (e, n) => Array.from(new Set(n.map((t) => t.getValue(e))).values()),
  vi = (e, n) => new Set(n.map((t) => t.getValue(e))).size,
  yi = (e, n) => n.length,
  Dt = {
    sum: ci,
    min: fi,
    max: gi,
    extent: pi,
    mean: mi,
    median: _i,
    unique: hi,
    uniqueCount: vi,
    count: yi,
  },
  bi = {
    getDefaultColumnDef: () => ({
      aggregatedCell: (e) => {
        var n, t;
        return (n =
          (t = e.getValue()) == null || t.toString == null
            ? void 0
            : t.toString()) != null
          ? n
          : null;
      },
      aggregationFn: "auto",
    }),
    getInitialState: (e) => ({ grouping: [], ...e }),
    getDefaultOptions: (e) => ({
      onGroupingChange: X("grouping", e),
      groupedColumnMode: "reorder",
    }),
    createColumn: (e, n) => ({
      toggleGrouping: () => {
        n.setGrouping((t) =>
          t != null && t.includes(e.id)
            ? t.filter((r) => r !== e.id)
            : [...(t ?? []), e.id]
        );
      },
      getCanGroup: () => {
        var t, r, o, i;
        return (t =
          (r =
            (o = (i = e.columnDef.enableGrouping) != null ? i : !0) != null
              ? o
              : n.options.enableGrouping) != null
            ? r
            : !0) != null
          ? t
          : !!e.accessorFn;
      },
      getIsGrouped: () => {
        var t;
        return (t = n.getState().grouping) == null ? void 0 : t.includes(e.id);
      },
      getGroupedIndex: () => {
        var t;
        return (t = n.getState().grouping) == null ? void 0 : t.indexOf(e.id);
      },
      getToggleGroupingHandler: () => {
        let t = e.getCanGroup();
        return () => {
          t && e.toggleGrouping();
        };
      },
      getAutoAggregationFn: () => {
        let t = n.getCoreRowModel().flatRows[0],
          r = t?.getValue(e.id);
        if (typeof r == "number") return Dt.sum;
        if (Object.prototype.toString.call(r) === "[object Date]")
          return Dt.extent;
      },
      getAggregationFn: () => {
        var t, r;
        if (!e) throw new Error();
        return et(e.columnDef.aggregationFn)
          ? e.columnDef.aggregationFn
          : e.columnDef.aggregationFn === "auto"
          ? e.getAutoAggregationFn()
          : (t =
              (r = n.options.aggregationFns) == null
                ? void 0
                : r[e.columnDef.aggregationFn]) != null
          ? t
          : Dt[e.columnDef.aggregationFn];
      },
    }),
    createTable: (e) => ({
      setGrouping: (n) =>
        e.options.onGroupingChange == null
          ? void 0
          : e.options.onGroupingChange(n),
      resetGrouping: (n) => {
        var t, r;
        e.setGrouping(
          n
            ? []
            : (t = (r = e.initialState) == null ? void 0 : r.grouping) != null
            ? t
            : []
        );
      },
      getPreGroupedRowModel: () => e.getFilteredRowModel(),
      getGroupedRowModel: () => (
        !e._getGroupedRowModel &&
          e.options.getGroupedRowModel &&
          (e._getGroupedRowModel = e.options.getGroupedRowModel(e)),
        e.options.manualGrouping || !e._getGroupedRowModel
          ? e.getPreGroupedRowModel()
          : e._getGroupedRowModel()
      ),
    }),
    createRow: (e, n) => ({
      getIsGrouped: () => !!e.groupingColumnId,
      getGroupingValue: (t) => {
        if (e._groupingValuesCache.hasOwnProperty(t))
          return e._groupingValuesCache[t];
        let r = n.getColumn(t);
        return r != null && r.columnDef.getGroupingValue
          ? ((e._groupingValuesCache[t] = r.columnDef.getGroupingValue(
              e.original
            )),
            e._groupingValuesCache[t])
          : e.getValue(t);
      },
      _groupingValuesCache: {},
    }),
    createCell: (e, n, t, r) => ({
      getIsGrouped: () => n.getIsGrouped() && n.id === t.groupingColumnId,
      getIsPlaceholder: () => !e.getIsGrouped() && n.getIsGrouped(),
      getIsAggregated: () => {
        var o;
        return (
          !e.getIsGrouped() &&
          !e.getIsPlaceholder() &&
          !!((o = t.subRows) != null && o.length)
        );
      },
    }),
  };
function Si(e, n, t) {
  if (!(n != null && n.length) || !t) return e;
  let r = e.filter((i) => !n.includes(i.id));
  return t === "remove"
    ? r
    : [...n.map((i) => e.find((l) => l.id === i)).filter(Boolean), ...r];
}
var wi = {
    getInitialState: (e) => ({ columnOrder: [], ...e }),
    getDefaultOptions: (e) => ({ onColumnOrderChange: X("columnOrder", e) }),
    createTable: (e) => ({
      setColumnOrder: (n) =>
        e.options.onColumnOrderChange == null
          ? void 0
          : e.options.onColumnOrderChange(n),
      resetColumnOrder: (n) => {
        var t;
        e.setColumnOrder(
          n ? [] : (t = e.initialState.columnOrder) != null ? t : []
        );
      },
      _getOrderColumnsFn: y(
        () => [
          e.getState().columnOrder,
          e.getState().grouping,
          e.options.groupedColumnMode,
        ],
        (n, t, r) => (o) => {
          let i = [];
          if (!(n != null && n.length)) i = o;
          else {
            let l = [...n],
              u = [...o];
            for (; u.length && l.length; ) {
              let a = l.shift(),
                d = u.findIndex((s) => s.id === a);
              d > -1 && i.push(u.splice(d, 1)[0]);
            }
            i = [...i, ...u];
          }
          return Si(i, t, r);
        },
        { key: !1 }
      ),
    }),
  },
  Pt = 0,
  kt = 10,
  Ot = () => ({ pageIndex: Pt, pageSize: kt }),
  Ci = {
    getInitialState: (e) => ({
      ...e,
      pagination: { ...Ot(), ...e?.pagination },
    }),
    getDefaultOptions: (e) => ({ onPaginationChange: X("pagination", e) }),
    createTable: (e) => {
      let n = !1,
        t = !1;
      return {
        _autoResetPageIndex: () => {
          var r, o;
          if (!n) {
            e._queue(() => {
              n = !0;
            });
            return;
          }
          if (
            (r =
              (o = e.options.autoResetAll) != null
                ? o
                : e.options.autoResetPageIndex) != null
              ? r
              : !e.options.manualPagination
          ) {
            if (t) return;
            (t = !0),
              e._queue(() => {
                e.resetPageIndex(), (t = !1);
              });
          }
        },
        setPagination: (r) => {
          let o = (i) => pe(r, i);
          return e.options.onPaginationChange == null
            ? void 0
            : e.options.onPaginationChange(o);
        },
        resetPagination: (r) => {
          var o;
          e.setPagination(
            r ? Ot() : (o = e.initialState.pagination) != null ? o : Ot()
          );
        },
        setPageIndex: (r) => {
          e.setPagination((o) => {
            let i = pe(r, o.pageIndex),
              l =
                typeof e.options.pageCount > "u" || e.options.pageCount === -1
                  ? Number.MAX_SAFE_INTEGER
                  : e.options.pageCount - 1;
            return (i = Math.max(0, Math.min(i, l))), { ...o, pageIndex: i };
          });
        },
        resetPageIndex: (r) => {
          var o, i, l;
          e.setPageIndex(
            r
              ? Pt
              : (o =
                  (i = e.initialState) == null || (l = i.pagination) == null
                    ? void 0
                    : l.pageIndex) != null
              ? o
              : Pt
          );
        },
        resetPageSize: (r) => {
          var o, i, l;
          e.setPageSize(
            r
              ? kt
              : (o =
                  (i = e.initialState) == null || (l = i.pagination) == null
                    ? void 0
                    : l.pageSize) != null
              ? o
              : kt
          );
        },
        setPageSize: (r) => {
          e.setPagination((o) => {
            let i = Math.max(1, pe(r, o.pageSize)),
              l = o.pageSize * o.pageIndex,
              u = Math.floor(l / i);
            return { ...o, pageIndex: u, pageSize: i };
          });
        },
        setPageCount: (r) =>
          e.setPagination((o) => {
            var i;
            let l = pe(r, (i = e.options.pageCount) != null ? i : -1);
            return (
              typeof l == "number" && (l = Math.max(-1, l)),
              { ...o, pageCount: l }
            );
          }),
        getPageOptions: y(
          () => [e.getPageCount()],
          (r) => {
            let o = [];
            return (
              r && r > 0 && (o = [...new Array(r)].fill(null).map((i, l) => l)),
              o
            );
          },
          {
            key: !1,
            debug: () => {
              var r;
              return (r = e.options.debugAll) != null
                ? r
                : e.options.debugTable;
            },
          }
        ),
        getCanPreviousPage: () => e.getState().pagination.pageIndex > 0,
        getCanNextPage: () => {
          let { pageIndex: r } = e.getState().pagination,
            o = e.getPageCount();
          return o === -1 ? !0 : o === 0 ? !1 : r < o - 1;
        },
        previousPage: () => e.setPageIndex((r) => r - 1),
        nextPage: () => e.setPageIndex((r) => r + 1),
        getPrePaginationRowModel: () => e.getExpandedRowModel(),
        getPaginationRowModel: () => (
          !e._getPaginationRowModel &&
            e.options.getPaginationRowModel &&
            (e._getPaginationRowModel = e.options.getPaginationRowModel(e)),
          e.options.manualPagination || !e._getPaginationRowModel
            ? e.getPrePaginationRowModel()
            : e._getPaginationRowModel()
        ),
        getPageCount: () => {
          var r;
          return (r = e.options.pageCount) != null
            ? r
            : Math.ceil(
                e.getPrePaginationRowModel().rows.length /
                  e.getState().pagination.pageSize
              );
        },
      };
    },
  },
  At = () => ({ left: [], right: [] }),
  Ei = {
    getInitialState: (e) => ({ columnPinning: At(), ...e }),
    getDefaultOptions: (e) => ({
      onColumnPinningChange: X("columnPinning", e),
    }),
    createColumn: (e, n) => ({
      pin: (t) => {
        let r = e
          .getLeafColumns()
          .map((o) => o.id)
          .filter(Boolean);
        n.setColumnPinning((o) => {
          var i, l;
          if (t === "right") {
            var u, a;
            return {
              left: ((u = o?.left) != null ? u : []).filter(
                (g) => !(r != null && r.includes(g))
              ),
              right: [
                ...((a = o?.right) != null ? a : []).filter(
                  (g) => !(r != null && r.includes(g))
                ),
                ...r,
              ],
            };
          }
          if (t === "left") {
            var d, s;
            return {
              left: [
                ...((d = o?.left) != null ? d : []).filter(
                  (g) => !(r != null && r.includes(g))
                ),
                ...r,
              ],
              right: ((s = o?.right) != null ? s : []).filter(
                (g) => !(r != null && r.includes(g))
              ),
            };
          }
          return {
            left: ((i = o?.left) != null ? i : []).filter(
              (g) => !(r != null && r.includes(g))
            ),
            right: ((l = o?.right) != null ? l : []).filter(
              (g) => !(r != null && r.includes(g))
            ),
          };
        });
      },
      getCanPin: () =>
        e.getLeafColumns().some((r) => {
          var o, i;
          return (
            ((o = r.columnDef.enablePinning) != null ? o : !0) &&
            ((i = n.options.enablePinning) != null ? i : !0)
          );
        }),
      getIsPinned: () => {
        let t = e.getLeafColumns().map((u) => u.id),
          { left: r, right: o } = n.getState().columnPinning,
          i = t.some((u) => r?.includes(u)),
          l = t.some((u) => o?.includes(u));
        return i ? "left" : l ? "right" : !1;
      },
      getPinnedIndex: () => {
        var t, r, o;
        let i = e.getIsPinned();
        return i
          ? (t =
              (r = n.getState().columnPinning) == null || (o = r[i]) == null
                ? void 0
                : o.indexOf(e.id)) != null
            ? t
            : -1
          : 0;
      },
    }),
    createRow: (e, n) => ({
      getCenterVisibleCells: y(
        () => [
          e._getAllVisibleCells(),
          n.getState().columnPinning.left,
          n.getState().columnPinning.right,
        ],
        (t, r, o) => {
          let i = [...(r ?? []), ...(o ?? [])];
          return t.filter((l) => !i.includes(l.column.id));
        },
        {
          key: "row.getCenterVisibleCells",
          debug: () => {
            var t;
            return (t = n.options.debugAll) != null ? t : n.options.debugRows;
          },
        }
      ),
      getLeftVisibleCells: y(
        () => [e._getAllVisibleCells(), n.getState().columnPinning.left, ,],
        (t, r) =>
          (r ?? [])
            .map((i) => t.find((l) => l.column.id === i))
            .filter(Boolean)
            .map((i) => ({ ...i, position: "left" })),
        {
          key: "row.getLeftVisibleCells",
          debug: () => {
            var t;
            return (t = n.options.debugAll) != null ? t : n.options.debugRows;
          },
        }
      ),
      getRightVisibleCells: y(
        () => [e._getAllVisibleCells(), n.getState().columnPinning.right],
        (t, r) =>
          (r ?? [])
            .map((i) => t.find((l) => l.column.id === i))
            .filter(Boolean)
            .map((i) => ({ ...i, position: "right" })),
        {
          key: "row.getRightVisibleCells",
          debug: () => {
            var t;
            return (t = n.options.debugAll) != null ? t : n.options.debugRows;
          },
        }
      ),
    }),
    createTable: (e) => ({
      setColumnPinning: (n) =>
        e.options.onColumnPinningChange == null
          ? void 0
          : e.options.onColumnPinningChange(n),
      resetColumnPinning: (n) => {
        var t, r;
        return e.setColumnPinning(
          n
            ? At()
            : (t = (r = e.initialState) == null ? void 0 : r.columnPinning) !=
              null
            ? t
            : At()
        );
      },
      getIsSomeColumnsPinned: (n) => {
        var t;
        let r = e.getState().columnPinning;
        if (!n) {
          var o, i;
          return !!(
            ((o = r.left) != null && o.length) ||
            ((i = r.right) != null && i.length)
          );
        }
        return !!((t = r[n]) != null && t.length);
      },
      getLeftLeafColumns: y(
        () => [e.getAllLeafColumns(), e.getState().columnPinning.left],
        (n, t) =>
          (t ?? []).map((r) => n.find((o) => o.id === r)).filter(Boolean),
        {
          key: !1,
          debug: () => {
            var n;
            return (n = e.options.debugAll) != null
              ? n
              : e.options.debugColumns;
          },
        }
      ),
      getRightLeafColumns: y(
        () => [e.getAllLeafColumns(), e.getState().columnPinning.right],
        (n, t) =>
          (t ?? []).map((r) => n.find((o) => o.id === r)).filter(Boolean),
        {
          key: !1,
          debug: () => {
            var n;
            return (n = e.options.debugAll) != null
              ? n
              : e.options.debugColumns;
          },
        }
      ),
      getCenterLeafColumns: y(
        () => [
          e.getAllLeafColumns(),
          e.getState().columnPinning.left,
          e.getState().columnPinning.right,
        ],
        (n, t, r) => {
          let o = [...(t ?? []), ...(r ?? [])];
          return n.filter((i) => !o.includes(i.id));
        },
        {
          key: !1,
          debug: () => {
            var n;
            return (n = e.options.debugAll) != null
              ? n
              : e.options.debugColumns;
          },
        }
      ),
    }),
  },
  Ri = {
    getInitialState: (e) => ({ rowSelection: {}, ...e }),
    getDefaultOptions: (e) => ({
      onRowSelectionChange: X("rowSelection", e),
      enableRowSelection: !0,
      enableMultiRowSelection: !0,
      enableSubRowSelection: !0,
    }),
    createTable: (e) => ({
      setRowSelection: (n) =>
        e.options.onRowSelectionChange == null
          ? void 0
          : e.options.onRowSelectionChange(n),
      resetRowSelection: (n) => {
        var t;
        return e.setRowSelection(
          n ? {} : (t = e.initialState.rowSelection) != null ? t : {}
        );
      },
      toggleAllRowsSelected: (n) => {
        e.setRowSelection((t) => {
          n = typeof n < "u" ? n : !e.getIsAllRowsSelected();
          let r = { ...t },
            o = e.getPreGroupedRowModel().flatRows;
          return (
            n
              ? o.forEach((i) => {
                  i.getCanSelect() && (r[i.id] = !0);
                })
              : o.forEach((i) => {
                  delete r[i.id];
                }),
            r
          );
        });
      },
      toggleAllPageRowsSelected: (n) =>
        e.setRowSelection((t) => {
          let r = typeof n < "u" ? n : !e.getIsAllPageRowsSelected(),
            o = { ...t };
          return (
            e.getRowModel().rows.forEach((i) => {
              Ht(o, i.id, r, e);
            }),
            o
          );
        }),
      getPreSelectedRowModel: () => e.getCoreRowModel(),
      getSelectedRowModel: y(
        () => [e.getState().rowSelection, e.getCoreRowModel()],
        (n, t) =>
          Object.keys(n).length
            ? Nt(e, t)
            : { rows: [], flatRows: [], rowsById: {} },
        {
          key: !1,
          debug: () => {
            var n;
            return (n = e.options.debugAll) != null ? n : e.options.debugTable;
          },
        }
      ),
      getFilteredSelectedRowModel: y(
        () => [e.getState().rowSelection, e.getFilteredRowModel()],
        (n, t) =>
          Object.keys(n).length
            ? Nt(e, t)
            : { rows: [], flatRows: [], rowsById: {} },
        {
          key: "getFilteredSelectedRowModel",
          debug: () => {
            var n;
            return (n = e.options.debugAll) != null ? n : e.options.debugTable;
          },
        }
      ),
      getGroupedSelectedRowModel: y(
        () => [e.getState().rowSelection, e.getSortedRowModel()],
        (n, t) =>
          Object.keys(n).length
            ? Nt(e, t)
            : { rows: [], flatRows: [], rowsById: {} },
        {
          key: "getGroupedSelectedRowModel",
          debug: () => {
            var n;
            return (n = e.options.debugAll) != null ? n : e.options.debugTable;
          },
        }
      ),
      getIsAllRowsSelected: () => {
        let n = e.getFilteredRowModel().flatRows,
          { rowSelection: t } = e.getState(),
          r = !!(n.length && Object.keys(t).length);
        return r && n.some((o) => o.getCanSelect() && !t[o.id]) && (r = !1), r;
      },
      getIsAllPageRowsSelected: () => {
        let n = e
            .getPaginationRowModel()
            .flatRows.filter((o) => o.getCanSelect()),
          { rowSelection: t } = e.getState(),
          r = !!n.length;
        return r && n.some((o) => !t[o.id]) && (r = !1), r;
      },
      getIsSomeRowsSelected: () => {
        var n;
        let t = Object.keys(
          (n = e.getState().rowSelection) != null ? n : {}
        ).length;
        return t > 0 && t < e.getFilteredRowModel().flatRows.length;
      },
      getIsSomePageRowsSelected: () => {
        let n = e.getPaginationRowModel().flatRows;
        return e.getIsAllPageRowsSelected()
          ? !1
          : n
              .filter((t) => t.getCanSelect())
              .some((t) => t.getIsSelected() || t.getIsSomeSelected());
      },
      getToggleAllRowsSelectedHandler: () => (n) => {
        e.toggleAllRowsSelected(n.target.checked);
      },
      getToggleAllPageRowsSelectedHandler: () => (n) => {
        e.toggleAllPageRowsSelected(n.target.checked);
      },
    }),
    createRow: (e, n) => ({
      toggleSelected: (t) => {
        let r = e.getIsSelected();
        n.setRowSelection((o) => {
          if (((t = typeof t < "u" ? t : !r), r === t)) return o;
          let i = { ...o };
          return Ht(i, e.id, t, n), i;
        });
      },
      getIsSelected: () => {
        let { rowSelection: t } = n.getState();
        return Gt(e, t);
      },
      getIsSomeSelected: () => {
        let { rowSelection: t } = n.getState();
        return lr(e, t) === "some";
      },
      getIsAllSubRowsSelected: () => {
        let { rowSelection: t } = n.getState();
        return lr(e, t) === "all";
      },
      getCanSelect: () => {
        var t;
        return typeof n.options.enableRowSelection == "function"
          ? n.options.enableRowSelection(e)
          : (t = n.options.enableRowSelection) != null
          ? t
          : !0;
      },
      getCanSelectSubRows: () => {
        var t;
        return typeof n.options.enableSubRowSelection == "function"
          ? n.options.enableSubRowSelection(e)
          : (t = n.options.enableSubRowSelection) != null
          ? t
          : !0;
      },
      getCanMultiSelect: () => {
        var t;
        return typeof n.options.enableMultiRowSelection == "function"
          ? n.options.enableMultiRowSelection(e)
          : (t = n.options.enableMultiRowSelection) != null
          ? t
          : !0;
      },
      getToggleSelectedHandler: () => {
        let t = e.getCanSelect();
        return (r) => {
          var o;
          t && e.toggleSelected((o = r.target) == null ? void 0 : o.checked);
        };
      },
    }),
  },
  Ht = (e, n, t, r) => {
    var o;
    let i = r.getRow(n);
    t
      ? (i.getCanMultiSelect() || Object.keys(e).forEach((l) => delete e[l]),
        i.getCanSelect() && (e[n] = !0))
      : delete e[n],
      (o = i.subRows) != null &&
        o.length &&
        i.getCanSelectSubRows() &&
        i.subRows.forEach((l) => Ht(e, l.id, t, r));
  };
function Nt(e, n) {
  let t = e.getState().rowSelection,
    r = [],
    o = {},
    i = function (l, u) {
      return l
        .map((a) => {
          var d;
          let s = Gt(a, t);
          if (
            (s && (r.push(a), (o[a.id] = a)),
            (d = a.subRows) != null &&
              d.length &&
              (a = { ...a, subRows: i(a.subRows) }),
            s)
          )
            return a;
        })
        .filter(Boolean);
    };
  return { rows: i(n.rows), flatRows: r, rowsById: o };
}
function Gt(e, n) {
  var t;
  return (t = n[e.id]) != null ? t : !1;
}
function lr(e, n, t) {
  if (e.subRows && e.subRows.length) {
    let r = !0,
      o = !1;
    return (
      e.subRows.forEach((i) => {
        (o && !r) || (Gt(i, n) ? (o = !0) : (r = !1));
      }),
      r ? "all" : o ? "some" : !1
    );
  }
  return !1;
}
var Lt = /([0-9]+)/gm,
  xi = (e, n, t) =>
    _r(me(e.getValue(t)).toLowerCase(), me(n.getValue(t)).toLowerCase()),
  Fi = (e, n, t) => _r(me(e.getValue(t)), me(n.getValue(t))),
  Mi = (e, n, t) =>
    Bt(me(e.getValue(t)).toLowerCase(), me(n.getValue(t)).toLowerCase()),
  $i = (e, n, t) => Bt(me(e.getValue(t)), me(n.getValue(t))),
  Vi = (e, n, t) => {
    let r = e.getValue(t),
      o = n.getValue(t);
    return r > o ? 1 : r < o ? -1 : 0;
  },
  Ii = (e, n, t) => Bt(e.getValue(t), n.getValue(t));
function Bt(e, n) {
  return e === n ? 0 : e > n ? 1 : -1;
}
function me(e) {
  return typeof e == "number"
    ? isNaN(e) || e === 1 / 0 || e === -1 / 0
      ? ""
      : String(e)
    : typeof e == "string"
    ? e
    : "";
}
function _r(e, n) {
  let t = e.split(Lt).filter(Boolean),
    r = n.split(Lt).filter(Boolean);
  for (; t.length && r.length; ) {
    let o = t.shift(),
      i = r.shift(),
      l = parseInt(o, 10),
      u = parseInt(i, 10),
      a = [l, u].sort();
    if (isNaN(a[0])) {
      if (o > i) return 1;
      if (i > o) return -1;
      continue;
    }
    if (isNaN(a[1])) return isNaN(l) ? -1 : 1;
    if (l > u) return 1;
    if (u > l) return -1;
  }
  return t.length - r.length;
}
var Pe = {
    alphanumeric: xi,
    alphanumericCaseSensitive: Fi,
    text: Mi,
    textCaseSensitive: $i,
    datetime: Vi,
    basic: Ii,
  },
  Ti = {
    getInitialState: (e) => ({ sorting: [], ...e }),
    getDefaultColumnDef: () => ({ sortingFn: "auto", sortUndefined: 1 }),
    getDefaultOptions: (e) => ({
      onSortingChange: X("sorting", e),
      isMultiSortEvent: (n) => n.shiftKey,
    }),
    createColumn: (e, n) => ({
      getAutoSortingFn: () => {
        let t = n.getFilteredRowModel().flatRows.slice(10),
          r = !1;
        for (let o of t) {
          let i = o?.getValue(e.id);
          if (Object.prototype.toString.call(i) === "[object Date]")
            return Pe.datetime;
          if (typeof i == "string" && ((r = !0), i.split(Lt).length > 1))
            return Pe.alphanumeric;
        }
        return r ? Pe.text : Pe.basic;
      },
      getAutoSortDir: () => {
        let t = n.getFilteredRowModel().flatRows[0];
        return typeof t?.getValue(e.id) == "string" ? "asc" : "desc";
      },
      getSortingFn: () => {
        var t, r;
        if (!e) throw new Error();
        return et(e.columnDef.sortingFn)
          ? e.columnDef.sortingFn
          : e.columnDef.sortingFn === "auto"
          ? e.getAutoSortingFn()
          : (t =
              (r = n.options.sortingFns) == null
                ? void 0
                : r[e.columnDef.sortingFn]) != null
          ? t
          : Pe[e.columnDef.sortingFn];
      },
      toggleSorting: (t, r) => {
        let o = e.getNextSortingOrder(),
          i = typeof t < "u" && t !== null;
        n.setSorting((l) => {
          let u = l?.find((c) => c.id === e.id),
            a = l?.findIndex((c) => c.id === e.id),
            d = [],
            s,
            g = i ? t : o === "desc";
          if (
            (l != null && l.length && e.getCanMultiSort() && r
              ? u
                ? (s = "toggle")
                : (s = "add")
              : l != null && l.length && a !== l.length - 1
              ? (s = "replace")
              : u
              ? (s = "toggle")
              : (s = "replace"),
            s === "toggle" && (i || o || (s = "remove")),
            s === "add")
          ) {
            var f;
            (d = [...l, { id: e.id, desc: g }]),
              d.splice(
                0,
                d.length -
                  ((f = n.options.maxMultiSortColCount) != null
                    ? f
                    : Number.MAX_SAFE_INTEGER)
              );
          } else
            s === "toggle"
              ? (d = l.map((c) => (c.id === e.id ? { ...c, desc: g } : c)))
              : s === "remove"
              ? (d = l.filter((c) => c.id !== e.id))
              : (d = [{ id: e.id, desc: g }]);
          return d;
        });
      },
      getFirstSortDir: () => {
        var t, r;
        return (
          (t =
            (r = e.columnDef.sortDescFirst) != null
              ? r
              : n.options.sortDescFirst) != null
            ? t
            : e.getAutoSortDir() === "desc"
        )
          ? "desc"
          : "asc";
      },
      getNextSortingOrder: (t) => {
        var r, o;
        let i = e.getFirstSortDir(),
          l = e.getIsSorted();
        return l
          ? l !== i &&
            ((r = n.options.enableSortingRemoval) == null || r) &&
            (!(t && (o = n.options.enableMultiRemove) != null) || o)
            ? !1
            : l === "desc"
            ? "asc"
            : "desc"
          : i;
      },
      getCanSort: () => {
        var t, r;
        return (
          ((t = e.columnDef.enableSorting) != null ? t : !0) &&
          ((r = n.options.enableSorting) != null ? r : !0) &&
          !!e.accessorFn
        );
      },
      getCanMultiSort: () => {
        var t, r;
        return (t =
          (r = e.columnDef.enableMultiSort) != null
            ? r
            : n.options.enableMultiSort) != null
          ? t
          : !!e.accessorFn;
      },
      getIsSorted: () => {
        var t;
        let r =
          (t = n.getState().sorting) == null
            ? void 0
            : t.find((o) => o.id === e.id);
        return r ? (r.desc ? "desc" : "asc") : !1;
      },
      getSortIndex: () => {
        var t, r;
        return (t =
          (r = n.getState().sorting) == null
            ? void 0
            : r.findIndex((o) => o.id === e.id)) != null
          ? t
          : -1;
      },
      clearSorting: () => {
        n.setSorting((t) =>
          t != null && t.length ? t.filter((r) => r.id !== e.id) : []
        );
      },
      getToggleSortingHandler: () => {
        let t = e.getCanSort();
        return (r) => {
          t &&
            (r.persist == null || r.persist(),
            e.toggleSorting == null ||
              e.toggleSorting(
                void 0,
                e.getCanMultiSort()
                  ? n.options.isMultiSortEvent == null
                    ? void 0
                    : n.options.isMultiSortEvent(r)
                  : !1
              ));
        };
      },
    }),
    createTable: (e) => ({
      setSorting: (n) =>
        e.options.onSortingChange == null
          ? void 0
          : e.options.onSortingChange(n),
      resetSorting: (n) => {
        var t, r;
        e.setSorting(
          n
            ? []
            : (t = (r = e.initialState) == null ? void 0 : r.sorting) != null
            ? t
            : []
        );
      },
      getPreSortedRowModel: () => e.getGroupedRowModel(),
      getSortedRowModel: () => (
        !e._getSortedRowModel &&
          e.options.getSortedRowModel &&
          (e._getSortedRowModel = e.options.getSortedRowModel(e)),
        e.options.manualSorting || !e._getSortedRowModel
          ? e.getPreSortedRowModel()
          : e._getSortedRowModel()
      ),
    }),
  },
  Di = {
    getInitialState: (e) => ({ columnVisibility: {}, ...e }),
    getDefaultOptions: (e) => ({
      onColumnVisibilityChange: X("columnVisibility", e),
    }),
    createColumn: (e, n) => ({
      toggleVisibility: (t) => {
        e.getCanHide() &&
          n.setColumnVisibility((r) => ({
            ...r,
            [e.id]: t ?? !e.getIsVisible(),
          }));
      },
      getIsVisible: () => {
        var t, r;
        return (t =
          (r = n.getState().columnVisibility) == null ? void 0 : r[e.id]) !=
          null
          ? t
          : !0;
      },
      getCanHide: () => {
        var t, r;
        return (
          ((t = e.columnDef.enableHiding) != null ? t : !0) &&
          ((r = n.options.enableHiding) != null ? r : !0)
        );
      },
      getToggleVisibilityHandler: () => (t) => {
        e.toggleVisibility == null || e.toggleVisibility(t.target.checked);
      },
    }),
    createRow: (e, n) => ({
      _getAllVisibleCells: y(
        () => [e.getAllCells(), n.getState().columnVisibility],
        (t) => t.filter((r) => r.column.getIsVisible()),
        {
          key: "row._getAllVisibleCells",
          debug: () => {
            var t;
            return (t = n.options.debugAll) != null ? t : n.options.debugRows;
          },
        }
      ),
      getVisibleCells: y(
        () => [
          e.getLeftVisibleCells(),
          e.getCenterVisibleCells(),
          e.getRightVisibleCells(),
        ],
        (t, r, o) => [...t, ...r, ...o],
        {
          key: !1,
          debug: () => {
            var t;
            return (t = n.options.debugAll) != null ? t : n.options.debugRows;
          },
        }
      ),
    }),
    createTable: (e) => {
      let n = (t, r) =>
        y(
          () => [
            r(),
            r()
              .filter((o) => o.getIsVisible())
              .map((o) => o.id)
              .join("_"),
          ],
          (o) =>
            o.filter((i) =>
              i.getIsVisible == null ? void 0 : i.getIsVisible()
            ),
          {
            key: t,
            debug: () => {
              var o;
              return (o = e.options.debugAll) != null
                ? o
                : e.options.debugColumns;
            },
          }
        );
      return {
        getVisibleFlatColumns: n("getVisibleFlatColumns", () =>
          e.getAllFlatColumns()
        ),
        getVisibleLeafColumns: n("getVisibleLeafColumns", () =>
          e.getAllLeafColumns()
        ),
        getLeftVisibleLeafColumns: n("getLeftVisibleLeafColumns", () =>
          e.getLeftLeafColumns()
        ),
        getRightVisibleLeafColumns: n("getRightVisibleLeafColumns", () =>
          e.getRightLeafColumns()
        ),
        getCenterVisibleLeafColumns: n("getCenterVisibleLeafColumns", () =>
          e.getCenterLeafColumns()
        ),
        setColumnVisibility: (t) =>
          e.options.onColumnVisibilityChange == null
            ? void 0
            : e.options.onColumnVisibilityChange(t),
        resetColumnVisibility: (t) => {
          var r;
          e.setColumnVisibility(
            t ? {} : (r = e.initialState.columnVisibility) != null ? r : {}
          );
        },
        toggleAllColumnsVisible: (t) => {
          var r;
          (t = (r = t) != null ? r : !e.getIsAllColumnsVisible()),
            e.setColumnVisibility(
              e
                .getAllLeafColumns()
                .reduce(
                  (o, i) => ({
                    ...o,
                    [i.id]: t || !(i.getCanHide != null && i.getCanHide()),
                  }),
                  {}
                )
            );
        },
        getIsAllColumnsVisible: () =>
          !e
            .getAllLeafColumns()
            .some((t) => !(t.getIsVisible != null && t.getIsVisible())),
        getIsSomeColumnsVisible: () =>
          e
            .getAllLeafColumns()
            .some((t) => (t.getIsVisible == null ? void 0 : t.getIsVisible())),
        getToggleAllColumnsVisibilityHandler: () => (t) => {
          var r;
          e.toggleAllColumnsVisible(
            (r = t.target) == null ? void 0 : r.checked
          );
        },
      };
    },
  },
  sr = [li, Di, wi, Ei, di, Ti, bi, ui, Ci, Ri, si];
function hr(e) {
  var n;
  (e.debugAll || e.debugTable) && console.info("Creating Table Instance...");
  let t = { _features: sr },
    r = t._features.reduce(
      (s, g) =>
        Object.assign(
          s,
          g.getDefaultOptions == null ? void 0 : g.getDefaultOptions(t)
        ),
      {}
    ),
    o = (s) =>
      t.options.mergeOptions ? t.options.mergeOptions(r, s) : { ...r, ...s },
    l = { ...{}, ...((n = e.initialState) != null ? n : {}) };
  t._features.forEach((s) => {
    var g;
    l =
      (g = s.getInitialState == null ? void 0 : s.getInitialState(l)) != null
        ? g
        : l;
  });
  let u = [],
    a = !1,
    d = {
      _features: sr,
      options: { ...r, ...e },
      initialState: l,
      _queue: (s) => {
        u.push(s),
          a ||
            ((a = !0),
            Promise.resolve()
              .then(() => {
                for (; u.length; ) u.shift()();
                a = !1;
              })
              .catch((g) =>
                setTimeout(() => {
                  throw g;
                })
              ));
      },
      reset: () => {
        t.setState(t.initialState);
      },
      setOptions: (s) => {
        let g = pe(s, t.options);
        t.options = o(g);
      },
      getState: () => t.options.state,
      setState: (s) => {
        t.options.onStateChange == null || t.options.onStateChange(s);
      },
      _getRowId: (s, g, f) => {
        var c;
        return (c =
          t.options.getRowId == null ? void 0 : t.options.getRowId(s, g, f)) !=
          null
          ? c
          : `${f ? [f.id, g].join(".") : g}`;
      },
      getCoreRowModel: () => (
        t._getCoreRowModel ||
          (t._getCoreRowModel = t.options.getCoreRowModel(t)),
        t._getCoreRowModel()
      ),
      getRowModel: () => t.getPaginationRowModel(),
      getRow: (s) => {
        let g = t.getRowModel().rowsById[s];
        if (!g) throw new Error();
        return g;
      },
      _getDefaultColumnDef: y(
        () => [t.options.defaultColumn],
        (s) => {
          var g;
          return (
            (s = (g = s) != null ? g : {}),
            {
              header: (f) => {
                let c = f.header.column.columnDef;
                return c.accessorKey
                  ? c.accessorKey
                  : c.accessorFn
                  ? c.id
                  : null;
              },
              cell: (f) => {
                var c, p;
                return (c =
                  (p = f.renderValue()) == null || p.toString == null
                    ? void 0
                    : p.toString()) != null
                  ? c
                  : null;
              },
              ...t._features.reduce(
                (f, c) =>
                  Object.assign(
                    f,
                    c.getDefaultColumnDef == null
                      ? void 0
                      : c.getDefaultColumnDef()
                  ),
                {}
              ),
              ...s,
            }
          );
        },
        {
          debug: () => {
            var s;
            return (s = t.options.debugAll) != null
              ? s
              : t.options.debugColumns;
          },
          key: !1,
        }
      ),
      _getColumnDefs: () => t.options.columns,
      getAllColumns: y(
        () => [t._getColumnDefs()],
        (s) => {
          let g = function (f, c, p) {
            return (
              p === void 0 && (p = 0),
              f.map((m) => {
                let _ = ii(t, m, p, c),
                  v = m;
                return (_.columns = v.columns ? g(v.columns, _, p + 1) : []), _;
              })
            );
          };
          return g(s);
        },
        {
          key: !1,
          debug: () => {
            var s;
            return (s = t.options.debugAll) != null
              ? s
              : t.options.debugColumns;
          },
        }
      ),
      getAllFlatColumns: y(
        () => [t.getAllColumns()],
        (s) => s.flatMap((g) => g.getFlatColumns()),
        {
          key: !1,
          debug: () => {
            var s;
            return (s = t.options.debugAll) != null
              ? s
              : t.options.debugColumns;
          },
        }
      ),
      _getAllFlatColumnsById: y(
        () => [t.getAllFlatColumns()],
        (s) => s.reduce((g, f) => ((g[f.id] = f), g), {}),
        {
          key: !1,
          debug: () => {
            var s;
            return (s = t.options.debugAll) != null
              ? s
              : t.options.debugColumns;
          },
        }
      ),
      getAllLeafColumns: y(
        () => [t.getAllColumns(), t._getOrderColumnsFn()],
        (s, g) => {
          let f = s.flatMap((c) => c.getLeafColumns());
          return g(f);
        },
        {
          key: !1,
          debug: () => {
            var s;
            return (s = t.options.debugAll) != null
              ? s
              : t.options.debugColumns;
          },
        }
      ),
      getColumn: (s) => t._getAllFlatColumnsById()[s],
    };
  return (
    Object.assign(t, d),
    t._features.forEach((s) =>
      Object.assign(t, s.createTable == null ? void 0 : s.createTable(t))
    ),
    t
  );
}
function Oi(e, n, t, r) {
  let o = () => {
      var l;
      return (l = i.getValue()) != null ? l : e.options.renderFallbackValue;
    },
    i = {
      id: `${n.id}_${t.id}`,
      row: n,
      column: t,
      getValue: () => n.getValue(r),
      renderValue: o,
      getContext: y(
        () => [e, t, n, i],
        (l, u, a, d) => ({
          table: l,
          column: u,
          row: a,
          cell: d,
          getValue: d.getValue,
          renderValue: d.renderValue,
        }),
        { key: !1, debug: () => e.options.debugAll }
      ),
    };
  return (
    e._features.forEach((l) => {
      Object.assign(
        i,
        l.createCell == null ? void 0 : l.createCell(i, t, n, e)
      );
    }, {}),
    i
  );
}
var Ut = (e, n, t, r, o, i, l) => {
  let u = {
    id: n,
    index: r,
    original: t,
    depth: o,
    parentId: l,
    _valuesCache: {},
    _uniqueValuesCache: {},
    getValue: (a) => {
      if (u._valuesCache.hasOwnProperty(a)) return u._valuesCache[a];
      let d = e.getColumn(a);
      if (d != null && d.accessorFn)
        return (
          (u._valuesCache[a] = d.accessorFn(u.original, r)), u._valuesCache[a]
        );
    },
    getUniqueValues: (a) => {
      if (u._uniqueValuesCache.hasOwnProperty(a))
        return u._uniqueValuesCache[a];
      let d = e.getColumn(a);
      if (d != null && d.accessorFn)
        return d.columnDef.getUniqueValues
          ? ((u._uniqueValuesCache[a] = d.columnDef.getUniqueValues(
              u.original,
              r
            )),
            u._uniqueValuesCache[a])
          : ((u._uniqueValuesCache[a] = [u.getValue(a)]),
            u._uniqueValuesCache[a]);
    },
    renderValue: (a) => {
      var d;
      return (d = u.getValue(a)) != null ? d : e.options.renderFallbackValue;
    },
    subRows: i ?? [],
    getLeafRows: () => oi(u.subRows, (a) => a.subRows),
    getParentRow: () => (u.parentId ? e.getRow(u.parentId) : void 0),
    getParentRows: () => {
      let a = [],
        d = u;
      for (;;) {
        let s = d.getParentRow();
        if (!s) break;
        a.push(s), (d = s);
      }
      return a.reverse();
    },
    getAllCells: y(
      () => [e.getAllLeafColumns()],
      (a) => a.map((d) => Oi(e, u, d, d.id)),
      {
        key: !1,
        debug: () => {
          var a;
          return (a = e.options.debugAll) != null ? a : e.options.debugRows;
        },
      }
    ),
    _getAllCellsByColumnId: y(
      () => [u.getAllCells()],
      (a) => a.reduce((d, s) => ((d[s.column.id] = s), d), {}),
      {
        key: "row.getAllCellsByColumnId",
        debug: () => {
          var a;
          return (a = e.options.debugAll) != null ? a : e.options.debugRows;
        },
      }
    ),
  };
  for (let a = 0; a < e._features.length; a++) {
    let d = e._features[a];
    Object.assign(
      u,
      d == null || d.createRow == null ? void 0 : d.createRow(u, e)
    );
  }
  return u;
};
function vr() {
  return (e) =>
    y(
      () => [e.options.data],
      (n) => {
        let t = { rows: [], flatRows: [], rowsById: {} },
          r = function (o, i, l) {
            i === void 0 && (i = 0);
            let u = [];
            for (let d = 0; d < o.length; d++) {
              let s = Ut(e, e._getRowId(o[d], d, l), o[d], d, i, void 0, l?.id);
              if (
                (t.flatRows.push(s),
                (t.rowsById[s.id] = s),
                u.push(s),
                e.options.getSubRows)
              ) {
                var a;
                (s.originalSubRows = e.options.getSubRows(o[d], d)),
                  (a = s.originalSubRows) != null &&
                    a.length &&
                    (s.subRows = r(s.originalSubRows, i + 1, s));
              }
            }
            return u;
          };
        return (t.rows = r(n)), t;
      },
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugTable;
        },
        onChange: () => {
          e._autoResetPageIndex();
        },
      }
    );
}
function yr(e, n, t) {
  return t.options.filterFromLeafRows ? Ai(e, n, t) : Ni(e, n, t);
}
function Ai(e, n, t) {
  var r;
  let o = [],
    i = {},
    l = (r = t.options.maxLeafRowFilterDepth) != null ? r : 100,
    u = function (a, d) {
      d === void 0 && (d = 0);
      let s = [];
      for (let f = 0; f < a.length; f++) {
        var g;
        let c = a[f],
          p = Ut(t, c.id, c.original, c.index, c.depth, void 0, c.parentId);
        if (
          ((p.columnFilters = c.columnFilters),
          (g = c.subRows) != null && g.length && d < l)
        ) {
          if (
            ((p.subRows = u(c.subRows, d + 1)),
            (c = p),
            n(c) && !p.subRows.length)
          ) {
            s.push(c), (i[c.id] = c), (i[f] = c);
            continue;
          }
          if (n(c) || p.subRows.length) {
            s.push(c), (i[c.id] = c), (i[f] = c);
            continue;
          }
        } else (c = p), n(c) && (s.push(c), (i[c.id] = c), (i[f] = c));
      }
      return s;
    };
  return { rows: u(e), flatRows: o, rowsById: i };
}
function Ni(e, n, t) {
  var r;
  let o = [],
    i = {},
    l = (r = t.options.maxLeafRowFilterDepth) != null ? r : 100,
    u = function (a, d) {
      d === void 0 && (d = 0);
      let s = [];
      for (let f = 0; f < a.length; f++) {
        let c = a[f];
        if (n(c)) {
          var g;
          if ((g = c.subRows) != null && g.length && d < l) {
            let m = Ut(
              t,
              c.id,
              c.original,
              c.index,
              c.depth,
              void 0,
              c.parentId
            );
            (m.subRows = u(c.subRows, d + 1)), (c = m);
          }
          s.push(c), o.push(c), (i[c.id] = c);
        }
      }
      return s;
    };
  return { rows: u(e), flatRows: o, rowsById: i };
}
function br() {
  return (e) =>
    y(
      () => [
        e.getPreFilteredRowModel(),
        e.getState().columnFilters,
        e.getState().globalFilter,
      ],
      (n, t, r) => {
        if (!n.rows.length || (!(t != null && t.length) && !r)) {
          for (let f = 0; f < n.flatRows.length; f++)
            (n.flatRows[f].columnFilters = {}),
              (n.flatRows[f].columnFiltersMeta = {});
          return n;
        }
        let o = [],
          i = [];
        (t ?? []).forEach((f) => {
          var c;
          let p = e.getColumn(f.id);
          if (!p) return;
          let m = p.getFilterFn();
          m &&
            o.push({
              id: f.id,
              filterFn: m,
              resolvedValue:
                (c =
                  m.resolveFilterValue == null
                    ? void 0
                    : m.resolveFilterValue(f.value)) != null
                  ? c
                  : f.value,
            });
        });
        let l = t.map((f) => f.id),
          u = e.getGlobalFilterFn(),
          a = e.getAllLeafColumns().filter((f) => f.getCanGlobalFilter());
        r &&
          u &&
          a.length &&
          (l.push("__global__"),
          a.forEach((f) => {
            var c;
            i.push({
              id: f.id,
              filterFn: u,
              resolvedValue:
                (c =
                  u.resolveFilterValue == null
                    ? void 0
                    : u.resolveFilterValue(r)) != null
                  ? c
                  : r,
            });
          }));
        let d, s;
        for (let f = 0; f < n.flatRows.length; f++) {
          let c = n.flatRows[f];
          if (((c.columnFilters = {}), o.length))
            for (let p = 0; p < o.length; p++) {
              d = o[p];
              let m = d.id;
              c.columnFilters[m] = d.filterFn(c, m, d.resolvedValue, (_) => {
                c.columnFiltersMeta[m] = _;
              });
            }
          if (i.length) {
            for (let p = 0; p < i.length; p++) {
              s = i[p];
              let m = s.id;
              if (
                s.filterFn(c, m, s.resolvedValue, (_) => {
                  c.columnFiltersMeta[m] = _;
                })
              ) {
                c.columnFilters.__global__ = !0;
                break;
              }
            }
            c.columnFilters.__global__ !== !0 &&
              (c.columnFilters.__global__ = !1);
          }
        }
        let g = (f) => {
          for (let c = 0; c < l.length; c++)
            if (f.columnFilters[l[c]] === !1) return !1;
          return !0;
        };
        return yr(n.rows, g, e);
      },
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugTable;
        },
        onChange: () => {
          e._autoResetPageIndex();
        },
      }
    );
}
function Sr() {
  return (e, n) =>
    y(
      () => [
        e.getPreFilteredRowModel(),
        e.getState().columnFilters,
        e.getState().globalFilter,
        e.getFilteredRowModel(),
      ],
      (t, r, o) => {
        if (!t.rows.length || (!(r != null && r.length) && !o)) return t;
        let i = [
            ...r.map((u) => u.id).filter((u) => u !== n),
            o ? "__global__" : void 0,
          ].filter(Boolean),
          l = (u) => {
            for (let a = 0; a < i.length; a++)
              if (u.columnFilters[i[a]] === !1) return !1;
            return !0;
          };
        return yr(t.rows, l, e);
      },
      {
        key: !1,
        debug: () => {
          var t;
          return (t = e.options.debugAll) != null ? t : e.options.debugTable;
        },
        onChange: () => {},
      }
    );
}
function wr() {
  return (e, n) =>
    y(
      () => {
        var t;
        return [(t = e.getColumn(n)) == null ? void 0 : t.getFacetedRowModel()];
      },
      (t) => {
        if (!t) return new Map();
        let r = new Map();
        for (let i = 0; i < t.flatRows.length; i++) {
          let l = t.flatRows[i].getUniqueValues(n);
          for (let u = 0; u < l.length; u++) {
            let a = l[u];
            if (r.has(a)) {
              var o;
              r.set(a, ((o = r.get(a)) != null ? o : 0) + 1);
            } else r.set(a, 1);
          }
        }
        return r;
      },
      {
        key: !1,
        debug: () => {
          var t;
          return (t = e.options.debugAll) != null ? t : e.options.debugTable;
        },
        onChange: () => {},
      }
    );
}
function Cr() {
  return (e, n) =>
    y(
      () => {
        var t;
        return [(t = e.getColumn(n)) == null ? void 0 : t.getFacetedRowModel()];
      },
      (t) => {
        var r;
        if (!t) return;
        let o = (r = t.flatRows[0]) == null ? void 0 : r.getUniqueValues(n);
        if (typeof o > "u") return;
        let i = [o, o];
        for (let l = 0; l < t.flatRows.length; l++) {
          let u = t.flatRows[l].getUniqueValues(n);
          for (let a = 0; a < u.length; a++) {
            let d = u[a];
            d < i[0] ? (i[0] = d) : d > i[1] && (i[1] = d);
          }
        }
        return i;
      },
      {
        key: !1,
        debug: () => {
          var t;
          return (t = e.options.debugAll) != null ? t : e.options.debugTable;
        },
        onChange: () => {},
      }
    );
}
function Er() {
  return (e) =>
    y(
      () => [e.getState().sorting, e.getPreSortedRowModel()],
      (n, t) => {
        if (!t.rows.length || !(n != null && n.length)) return t;
        let r = e.getState().sorting,
          o = [],
          i = r.filter((a) => {
            var d;
            return (d = e.getColumn(a.id)) == null ? void 0 : d.getCanSort();
          }),
          l = {};
        i.forEach((a) => {
          let d = e.getColumn(a.id);
          d &&
            (l[a.id] = {
              sortUndefined: d.columnDef.sortUndefined,
              invertSorting: d.columnDef.invertSorting,
              sortingFn: d.getSortingFn(),
            });
        });
        let u = (a) => {
          let d = [...a];
          return (
            d.sort((s, g) => {
              for (let c = 0; c < i.length; c += 1) {
                var f;
                let p = i[c],
                  m = l[p.id],
                  _ = (f = p?.desc) != null ? f : !1,
                  v = 0;
                if (m.sortUndefined) {
                  let w = s.getValue(p.id),
                    x = g.getValue(p.id),
                    M = w === void 0,
                    I = x === void 0;
                  (M || I) &&
                    (v = M && I ? 0 : M ? m.sortUndefined : -m.sortUndefined);
                }
                if ((v === 0 && (v = m.sortingFn(s, g, p.id)), v !== 0))
                  return _ && (v *= -1), m.invertSorting && (v *= -1), v;
              }
              return s.index - g.index;
            }),
            d.forEach((s) => {
              var g;
              o.push(s),
                (g = s.subRows) != null &&
                  g.length &&
                  (s.subRows = u(s.subRows));
            }),
            d
          );
        };
        return { rows: u(t.rows), flatRows: o, rowsById: t.rowsById };
      },
      {
        key: !1,
        debug: () => {
          var n;
          return (n = e.options.debugAll) != null ? n : e.options.debugTable;
        },
        onChange: () => {
          e._autoResetPageIndex();
        },
      }
    );
}
function tt(e, n) {
  return e ? (Pi(e) ? G(e, n) : e) : null;
}
function Pi(e) {
  return ki(e) || typeof e == "function" || Hi(e);
}
function ki(e) {
  return (
    typeof e == "function" &&
    (() => {
      let n = Object.getPrototypeOf(e);
      return n.prototype && n.prototype.isReactComponent;
    })()
  );
}
function Hi(e) {
  return (
    typeof e == "object" &&
    typeof e.$$typeof == "symbol" &&
    ["react.memo", "react.forward_ref"].includes(e.$$typeof.description)
  );
}
function Rr(e) {
  let n = {
      state: {},
      onStateChange: () => {},
      renderFallbackValue: null,
      ...e,
    },
    [t] = D(() => ({ current: hr(n) })),
    [r, o] = D(() => t.current.initialState);
  return (
    t.current.setOptions((i) => ({
      ...i,
      ...e,
      state: { ...r, ...e.state },
      onStateChange: (l) => {
        o(l), e.onStateChange == null || e.onStateChange(l);
      },
    })),
    t.current
  );
}
function ke() {
  return (
    (ke = Object.assign
      ? Object.assign.bind()
      : function (e) {
          for (var n = 1; n < arguments.length; n++) {
            var t = arguments[n];
            for (var r in t)
              Object.prototype.hasOwnProperty.call(t, r) && (e[r] = t[r]);
          }
          return e;
        }),
    ke.apply(this, arguments)
  );
}
function He() {
  return (
    (He = Object.assign
      ? Object.assign.bind()
      : function (e) {
          for (var n = 1; n < arguments.length; n++) {
            var t = arguments[n];
            for (var r in t)
              Object.prototype.hasOwnProperty.call(t, r) && (e[r] = t[r]);
          }
          return e;
        }),
    He.apply(this, arguments)
  );
}
function he(e, n, t) {
  var r,
    o = (r = t.initialDeps) != null ? r : [],
    i;
  return function () {
    var l;
    t.key && t.debug != null && t.debug() && (l = Date.now());
    var u = e(),
      a =
        u.length !== o.length ||
        u.some(function (p, m) {
          return o[m] !== p;
        });
    if (!a) return i;
    o = u;
    var d;
    if (
      (t.key && t.debug != null && t.debug() && (d = Date.now()),
      (i = n.apply(void 0, u)),
      t.key && t.debug != null && t.debug())
    ) {
      var s = Math.round((Date.now() - l) * 100) / 100,
        g = Math.round((Date.now() - d) * 100) / 100,
        f = g / 16,
        c = function (m, _) {
          for (m = String(m); m.length < _; ) m = " " + m;
          return m;
        };
      console.info(
        "%c\u23F1 " + c(g, 5) + " /" + c(s, 5) + " ms",
        `
            font-size: .6rem;
            font-weight: bold;
            color: hsl(` +
          Math.max(0, Math.min(120 - 120 * f, 120)) +
          "deg 100% 31%);",
        t?.key
      );
    }
    return t == null || t.onChange == null || t.onChange(i), i;
  };
}
function nt(e, n) {
  if (e === void 0)
    throw new Error("Unexpected undefined" + (n ? ": " + n : ""));
  return e;
}
var xr = function (n, t) {
  return Math.abs(n - t) < 1;
};
var Li = function (n) {
    return n;
  },
  zi = function (n) {
    for (
      var t = Math.max(n.startIndex - n.overscan, 0),
        r = Math.min(n.endIndex + n.overscan, n.count - 1),
        o = [],
        i = t;
      i <= r;
      i++
    )
      o.push(i);
    return o;
  },
  Fr = function (n, t) {
    var r = n.scrollElement;
    if (r) {
      var o = function (u) {
        var a = u.width,
          d = u.height;
        t({ width: Math.round(a), height: Math.round(d) });
      };
      o(r.getBoundingClientRect());
      var i = new ResizeObserver(function (l) {
        var u = l[0];
        if (u != null && u.borderBoxSize) {
          var a = u.borderBoxSize[0];
          if (a) {
            o({ width: a.inlineSize, height: a.blockSize });
            return;
          }
        }
        o(r.getBoundingClientRect());
      });
      return (
        i.observe(r, { box: "border-box" }),
        function () {
          i.unobserve(r);
        }
      );
    }
  };
var Mr = function (n, t) {
  var r = n.scrollElement;
  if (r) {
    var o = function () {
      t(r[n.options.horizontal ? "scrollLeft" : "scrollTop"]);
    };
    return (
      o(),
      r.addEventListener("scroll", o, { passive: !0 }),
      function () {
        r.removeEventListener("scroll", o);
      }
    );
  }
};
var Gi = function (n, t, r) {
  if (t != null && t.borderBoxSize) {
    var o = t.borderBoxSize[0];
    if (o) {
      var i = Math.round(o[r.options.horizontal ? "inlineSize" : "blockSize"]);
      return i;
    }
  }
  return Math.round(
    n.getBoundingClientRect()[r.options.horizontal ? "width" : "height"]
  );
};
var $r = function (n, t, r) {
    var o,
      i,
      l = t.adjustments,
      u = l === void 0 ? 0 : l,
      a = t.behavior,
      d = n + u;
    (o = r.scrollElement) == null ||
      o.scrollTo == null ||
      o.scrollTo(
        ((i = {}),
        (i[r.options.horizontal ? "left" : "top"] = d),
        (i.behavior = a),
        i)
      );
  },
  Vr = function (n) {
    var t = this;
    (this.unsubs = []),
      (this.scrollElement = null),
      (this.isScrolling = !1),
      (this.isScrollingTimeoutId = null),
      (this.scrollToIndexTimeoutId = null),
      (this.measurementsCache = []),
      (this.itemSizeCache = new Map()),
      (this.pendingMeasuredCacheIndexes = []),
      (this.scrollDirection = null),
      (this.scrollAdjustments = 0),
      (this.measureElementCache = new Map()),
      (this.observer = (function () {
        var r = null,
          o = function () {
            return (
              r ||
              (typeof ResizeObserver < "u"
                ? (r = new ResizeObserver(function (l) {
                    l.forEach(function (u) {
                      t._measureElement(u.target, u);
                    });
                  }))
                : null)
            );
          };
        return {
          disconnect: function () {
            var l;
            return (l = o()) == null ? void 0 : l.disconnect();
          },
          observe: function (l) {
            var u;
            return (u = o()) == null
              ? void 0
              : u.observe(l, { box: "border-box" });
          },
          unobserve: function (l) {
            var u;
            return (u = o()) == null ? void 0 : u.unobserve(l);
          },
        };
      })()),
      (this.range = { startIndex: 0, endIndex: 0 }),
      (this.setOptions = function (r) {
        Object.entries(r).forEach(function (o) {
          var i = o[0],
            l = o[1];
          typeof l > "u" && delete r[i];
        }),
          (t.options = He(
            {
              debug: !1,
              initialOffset: 0,
              overscan: 1,
              paddingStart: 0,
              paddingEnd: 0,
              scrollPaddingStart: 0,
              scrollPaddingEnd: 0,
              horizontal: !1,
              getItemKey: Li,
              rangeExtractor: zi,
              onChange: function () {},
              measureElement: Gi,
              initialRect: { width: 0, height: 0 },
              scrollMargin: 0,
              scrollingDelay: 150,
              indexAttribute: "data-index",
              initialMeasurementsCache: [],
              lanes: 1,
            },
            r
          ));
      }),
      (this.notify = function () {
        t.options.onChange == null || t.options.onChange(t);
      }),
      (this.cleanup = function () {
        t.unsubs.filter(Boolean).forEach(function (r) {
          return r();
        }),
          (t.unsubs = []),
          (t.scrollElement = null);
      }),
      (this._didMount = function () {
        return (
          t.measureElementCache.forEach(t.observer.observe),
          function () {
            t.observer.disconnect(), t.cleanup();
          }
        );
      }),
      (this._willUpdate = function () {
        var r = t.options.getScrollElement();
        t.scrollElement !== r &&
          (t.cleanup(),
          (t.scrollElement = r),
          t._scrollToOffset(t.scrollOffset, {
            adjustments: void 0,
            behavior: void 0,
          }),
          t.unsubs.push(
            t.options.observeElementRect(t, function (o) {
              var i = t.scrollRect;
              (t.scrollRect = o),
                (t.options.horizontal
                  ? o.width !== i.width
                  : o.height !== i.height) && t.maybeNotify();
            })
          ),
          t.unsubs.push(
            t.options.observeElementOffset(t, function (o) {
              (t.scrollAdjustments = 0),
                t.scrollOffset !== o &&
                  (t.isScrollingTimeoutId !== null &&
                    (clearTimeout(t.isScrollingTimeoutId),
                    (t.isScrollingTimeoutId = null)),
                  (t.isScrolling = !0),
                  (t.scrollDirection =
                    t.scrollOffset < o ? "forward" : "backward"),
                  (t.scrollOffset = o),
                  t.maybeNotify(),
                  (t.isScrollingTimeoutId = setTimeout(function () {
                    (t.isScrollingTimeoutId = null),
                      (t.isScrolling = !1),
                      (t.scrollDirection = null),
                      t.maybeNotify();
                  }, t.options.scrollingDelay)));
            })
          ));
      }),
      (this.getSize = function () {
        return t.scrollRect[t.options.horizontal ? "width" : "height"];
      }),
      (this.memoOptions = he(
        function () {
          return [
            t.options.count,
            t.options.paddingStart,
            t.options.scrollMargin,
            t.options.getItemKey,
          ];
        },
        function (r, o, i, l) {
          return (
            (t.pendingMeasuredCacheIndexes = []),
            { count: r, paddingStart: o, scrollMargin: i, getItemKey: l }
          );
        },
        { key: !1 }
      )),
      (this.getFurthestMeasurement = function (r, o) {
        for (var i = new Map(), l = new Map(), u = o - 1; u >= 0; u--) {
          var a = r[u];
          if (!i.has(a.lane)) {
            var d = l.get(a.lane);
            if (
              (d == null || a.end > d.end
                ? l.set(a.lane, a)
                : a.end < d.end && i.set(a.lane, !0),
              i.size === t.options.lanes)
            )
              break;
          }
        }
        return l.size === t.options.lanes
          ? Array.from(l.values()).sort(function (s, g) {
              return s.end - g.end;
            })[0]
          : void 0;
      }),
      (this.getMeasurements = he(
        function () {
          return [t.memoOptions(), t.itemSizeCache];
        },
        function (r, o) {
          var i = r.count,
            l = r.paddingStart,
            u = r.scrollMargin,
            a = r.getItemKey,
            d =
              t.pendingMeasuredCacheIndexes.length > 0
                ? Math.min.apply(Math, t.pendingMeasuredCacheIndexes)
                : 0;
          t.pendingMeasuredCacheIndexes = [];
          for (var s = t.measurementsCache.slice(0, d), g = d; g < i; g++) {
            var f = a(g),
              c =
                t.options.lanes === 1
                  ? s[g - 1]
                  : t.getFurthestMeasurement(s, g),
              p = c ? c.end : l + u,
              m = o.get(f),
              _ = typeof m == "number" ? m : t.options.estimateSize(g),
              v = p + _,
              w = c ? c.lane : g % t.options.lanes;
            s[g] = { index: g, start: p, size: _, end: v, key: f, lane: w };
          }
          return (t.measurementsCache = s), s;
        },
        {
          key: !1,
          debug: function () {
            return t.options.debug;
          },
        }
      )),
      (this.calculateRange = he(
        function () {
          return [t.getMeasurements(), t.getSize(), t.scrollOffset];
        },
        function (r, o, i) {
          return (t.range = Bi({
            measurements: r,
            outerSize: o,
            scrollOffset: i,
          }));
        },
        {
          key: !1,
          debug: function () {
            return t.options.debug;
          },
        }
      )),
      (this.maybeNotify = he(
        function () {
          var r = t.calculateRange();
          return [r.startIndex, r.endIndex, t.isScrolling];
        },
        function () {
          t.notify();
        },
        {
          key: !1,
          debug: function () {
            return t.options.debug;
          },
          initialDeps: [
            this.range.startIndex,
            this.range.endIndex,
            this.isScrolling,
          ],
        }
      )),
      (this.getIndexes = he(
        function () {
          return [
            t.options.rangeExtractor,
            t.calculateRange(),
            t.options.overscan,
            t.options.count,
          ];
        },
        function (r, o, i, l) {
          return r(He({}, o, { overscan: i, count: l }));
        },
        {
          key: !1,
          debug: function () {
            return t.options.debug;
          },
        }
      )),
      (this.indexFromElement = function (r) {
        var o = t.options.indexAttribute,
          i = r.getAttribute(o);
        return i
          ? parseInt(i, 10)
          : (console.warn(
              "Missing attribute name '" + o + "={index}' on measured element."
            ),
            -1);
      }),
      (this._measureElement = function (r, o) {
        var i,
          l = t.indexFromElement(r),
          u = t.measurementsCache[l];
        if (u) {
          var a = t.measureElementCache.get(u.key);
          if (!r.isConnected) {
            t.observer.unobserve(r),
              r === a && t.measureElementCache.delete(u.key);
            return;
          }
          a !== r &&
            (a && t.observer.unobserve(a),
            t.observer.observe(r),
            t.measureElementCache.set(u.key, r));
          var d = t.options.measureElement(r, o, t),
            s = (i = t.itemSizeCache.get(u.key)) != null ? i : u.size,
            g = d - s;
          g !== 0 &&
            (u.start < t.scrollOffset &&
              t._scrollToOffset(t.scrollOffset, {
                adjustments: (t.scrollAdjustments += g),
                behavior: void 0,
              }),
            t.pendingMeasuredCacheIndexes.push(l),
            (t.itemSizeCache = new Map(t.itemSizeCache.set(u.key, d))),
            t.notify());
        }
      }),
      (this.measureElement = function (r) {
        r && t._measureElement(r, void 0);
      }),
      (this.getVirtualItems = he(
        function () {
          return [t.getIndexes(), t.getMeasurements()];
        },
        function (r, o) {
          for (var i = [], l = 0, u = r.length; l < u; l++) {
            var a = r[l],
              d = o[a];
            i.push(d);
          }
          return i;
        },
        {
          key: !1,
          debug: function () {
            return t.options.debug;
          },
        }
      )),
      (this.getVirtualItemForOffset = function (r) {
        var o = t.getMeasurements();
        return nt(
          o[
            Ir(
              0,
              o.length - 1,
              function (i) {
                return nt(o[i]).start;
              },
              r
            )
          ]
        );
      }),
      (this.getOffsetForAlignment = function (r, o) {
        var i = t.getSize();
        o === "auto" &&
          (r <= t.scrollOffset
            ? (o = "start")
            : r >= t.scrollOffset + i
            ? (o = "end")
            : (o = "start")),
          o === "start"
            ? (r = r)
            : o === "end"
            ? (r = r - i)
            : o === "center" && (r = r - i / 2);
        var l = t.options.horizontal ? "scrollWidth" : "scrollHeight",
          u = t.scrollElement
            ? "document" in t.scrollElement
              ? t.scrollElement.document.documentElement[l]
              : t.scrollElement[l]
            : 0,
          a = u - t.getSize();
        return Math.max(Math.min(a, r), 0);
      }),
      (this.getOffsetForIndex = function (r, o) {
        o === void 0 && (o = "auto"),
          (r = Math.max(0, Math.min(r, t.options.count - 1)));
        var i = nt(t.getMeasurements()[r]);
        if (o === "auto")
          if (
            i.end >=
            t.scrollOffset + t.getSize() - t.options.scrollPaddingEnd
          )
            o = "end";
          else if (i.start <= t.scrollOffset + t.options.scrollPaddingStart)
            o = "start";
          else return [t.scrollOffset, o];
        var l =
          o === "end"
            ? i.end + t.options.scrollPaddingEnd
            : i.start - t.options.scrollPaddingStart;
        return [t.getOffsetForAlignment(l, o), o];
      }),
      (this.isDynamicMode = function () {
        return t.measureElementCache.size > 0;
      }),
      (this.cancelScrollToIndex = function () {
        t.scrollToIndexTimeoutId !== null &&
          (clearTimeout(t.scrollToIndexTimeoutId),
          (t.scrollToIndexTimeoutId = null));
      }),
      (this.scrollToOffset = function (r, o) {
        var i = o === void 0 ? {} : o,
          l = i.align,
          u = l === void 0 ? "start" : l,
          a = i.behavior;
        t.cancelScrollToIndex(),
          a === "smooth" &&
            t.isDynamicMode() &&
            console.warn(
              "The `smooth` scroll behavior is not fully supported with dynamic size."
            ),
          t._scrollToOffset(t.getOffsetForAlignment(r, u), {
            adjustments: void 0,
            behavior: a,
          });
      }),
      (this.scrollToIndex = function (r, o) {
        var i = o === void 0 ? {} : o,
          l = i.align,
          u = l === void 0 ? "auto" : l,
          a = i.behavior;
        (r = Math.max(0, Math.min(r, t.options.count - 1))),
          t.cancelScrollToIndex(),
          a === "smooth" &&
            t.isDynamicMode() &&
            console.warn(
              "The `smooth` scroll behavior is not fully supported with dynamic size."
            );
        var d = t.getOffsetForIndex(r, u),
          s = d[0],
          g = d[1];
        t._scrollToOffset(s, { adjustments: void 0, behavior: a }),
          a !== "smooth" &&
            t.isDynamicMode() &&
            (t.scrollToIndexTimeoutId = setTimeout(function () {
              t.scrollToIndexTimeoutId = null;
              var f = t.measureElementCache.has(t.options.getItemKey(r));
              if (f) {
                var c = t.getOffsetForIndex(r, g),
                  p = c[0];
                xr(p, t.scrollOffset) ||
                  t.scrollToIndex(r, { align: g, behavior: a });
              } else t.scrollToIndex(r, { align: g, behavior: a });
            }));
      }),
      (this.scrollBy = function (r, o) {
        var i = o === void 0 ? {} : o,
          l = i.behavior;
        t.cancelScrollToIndex(),
          l === "smooth" &&
            t.isDynamicMode() &&
            console.warn(
              "The `smooth` scroll behavior is not fully supported with dynamic size."
            ),
          t._scrollToOffset(t.scrollOffset + r, {
            adjustments: void 0,
            behavior: l,
          });
      }),
      (this.getTotalSize = function () {
        var r;
        return (
          (((r = t.getMeasurements()[t.options.count - 1]) == null
            ? void 0
            : r.end) || t.options.paddingStart) -
          t.options.scrollMargin +
          t.options.paddingEnd
        );
      }),
      (this._scrollToOffset = function (r, o) {
        var i = o.adjustments,
          l = o.behavior;
        t.options.scrollToFn(r, { behavior: l, adjustments: i }, t);
      }),
      (this.measure = function () {
        (t.itemSizeCache = new Map()), t.notify();
      }),
      this.setOptions(n),
      (this.scrollRect = this.options.initialRect),
      (this.scrollOffset = this.options.initialOffset),
      (this.measurementsCache = this.options.initialMeasurementsCache),
      this.measurementsCache.forEach(function (r) {
        t.itemSizeCache.set(r.key, r.size);
      }),
      this.maybeNotify();
  },
  Ir = function (n, t, r, o) {
    for (; n <= t; ) {
      var i = ((n + t) / 2) | 0,
        l = r(i);
      if (l < o) n = i + 1;
      else if (l > o) t = i - 1;
      else return i;
    }
    return n > 0 ? n - 1 : 0;
  };
function Bi(e) {
  for (
    var n = e.measurements,
      t = e.outerSize,
      r = e.scrollOffset,
      o = n.length - 1,
      i = function (d) {
        return n[d].start;
      },
      l = Ir(0, o, i, r),
      u = l;
    u < o && n[u].end < r + t;

  )
    u++;
  return { startIndex: l, endIndex: u };
}
var Ui = typeof document < "u" ? re : L;
function ji(e) {
  var n = xe(function () {
      return {};
    }, {})[1],
    t = ke({}, e, {
      onChange: function (l) {
        n(), e.onChange == null || e.onChange(l);
      },
    }),
    r = D(function () {
      return new Vr(t);
    }),
    o = r[0];
  return (
    o.setOptions(t),
    L(function () {
      return o._didMount();
    }, []),
    Ui(function () {
      return o._willUpdate();
    }),
    o
  );
}
function Tr(e) {
  return ji(
    ke({ observeElementRect: Fr, observeElementOffset: Mr, scrollToFn: $r }, e)
  );
}
function Dr(e) {
  return {
    render(n) {
      Ft(n, e);
    },
    unmount() {
      $t(e);
    },
  };
}
var Hr = Symbol.for("immer-nothing"),
  Or = Symbol.for("immer-draftable"),
  C = Symbol.for("immer-state");
function Y(e, ...n) {
  throw new Error(
    `[Immer] minified error nr: ${e}. Full error at: https://bit.ly/3cXEKWf`
  );
}
var Fe = Object.getPrototypeOf;
function Me(e) {
  return !!e && !!e[C];
}
function de(e) {
  return e
    ? Lr(e) ||
        Array.isArray(e) ||
        !!e[Or] ||
        !!e.constructor?.[Or] ||
        st(e) ||
        at(e)
    : !1;
}
var Ki = Object.prototype.constructor.toString();
function Lr(e) {
  if (!e || typeof e != "object") return !1;
  let n = Fe(e);
  if (n === null) return !0;
  let t = Object.hasOwnProperty.call(n, "constructor") && n.constructor;
  return t === Object
    ? !0
    : typeof t == "function" && Function.toString.call(t) === Ki;
}
function $e(e, n) {
  lt(e) === 0
    ? Object.entries(e).forEach(([t, r]) => {
        n(t, r, e);
      })
    : e.forEach((t, r) => n(r, t, e));
}
function lt(e) {
  let n = e[C];
  return n ? n.type_ : Array.isArray(e) ? 1 : st(e) ? 2 : at(e) ? 3 : 0;
}
function qt(e, n) {
  return lt(e) === 2 ? e.has(n) : Object.prototype.hasOwnProperty.call(e, n);
}
function zr(e, n, t) {
  let r = lt(e);
  r === 2 ? e.set(n, t) : r === 3 ? e.add(t) : (e[n] = t);
}
function qi(e, n) {
  return e === n ? e !== 0 || 1 / e === 1 / n : e !== e && n !== n;
}
function st(e) {
  return e instanceof Map;
}
function at(e) {
  return e instanceof Set;
}
function k(e) {
  return e.copy_ || e.base_;
}
function Wt(e, n) {
  if (st(e)) return new Map(e);
  if (at(e)) return new Set(e);
  if (Array.isArray(e)) return Array.prototype.slice.call(e);
  if (!n && Lr(e))
    return Fe(e) ? { ...e } : Object.assign(Object.create(null), e);
  let t = Object.getOwnPropertyDescriptors(e);
  delete t[C];
  let r = Reflect.ownKeys(t);
  for (let o = 0; o < r.length; o++) {
    let i = r[o],
      l = t[i];
    l.writable === !1 && ((l.writable = !0), (l.configurable = !0)),
      (l.get || l.set) &&
        (t[i] = {
          configurable: !0,
          writable: !0,
          enumerable: l.enumerable,
          value: e[i],
        });
  }
  return Object.create(Fe(e), t);
}
function Ve(e, n = !1) {
  return (
    ut(e) ||
      Me(e) ||
      !de(e) ||
      (lt(e) > 1 && (e.set = e.add = e.clear = e.delete = Wi),
      Object.freeze(e),
      n && $e(e, (t, r) => Ve(r, !0), !0)),
    e
  );
}
function Wi() {
  Y(2);
}
function ut(e) {
  return Object.isFrozen(e);
}
var Xt = {};
function ve(e) {
  let n = Xt[e];
  return n || Y(0, e), n;
}
function Xi(e, n) {
  Xt[e] || (Xt[e] = n);
}
var Le;
function rt() {
  return Le;
}
function Yi(e, n) {
  return {
    drafts_: [],
    parent_: e,
    immer_: n,
    canAutoFreeze_: !0,
    unfinalizedDrafts_: 0,
  };
}
function Ar(e, n) {
  n &&
    (ve("Patches"),
    (e.patches_ = []),
    (e.inversePatches_ = []),
    (e.patchListener_ = n));
}
function Yt(e) {
  Jt(e), e.drafts_.forEach(Ji), (e.drafts_ = null);
}
function Jt(e) {
  e === Le && (Le = e.parent_);
}
function Nr(e) {
  return (Le = Yi(Le, e));
}
function Ji(e) {
  let n = e[C];
  n.type_ === 0 || n.type_ === 1 ? n.revoke_() : (n.revoked_ = !0);
}
function Pr(e, n) {
  n.unfinalizedDrafts_ = n.drafts_.length;
  let t = n.drafts_[0];
  return (
    e !== void 0 && e !== t
      ? (t[C].modified_ && (Yt(n), Y(4)),
        de(e) && ((e = ot(n, e)), n.parent_ || it(n, e)),
        n.patches_ &&
          ve("Patches").generateReplacementPatches_(
            t[C].base_,
            e,
            n.patches_,
            n.inversePatches_
          ))
      : (e = ot(n, t, [])),
    Yt(n),
    n.patches_ && n.patchListener_(n.patches_, n.inversePatches_),
    e !== Hr ? e : void 0
  );
}
function ot(e, n, t) {
  if (ut(n)) return n;
  let r = n[C];
  if (!r) return $e(n, (o, i) => kr(e, r, n, o, i, t), !0), n;
  if (r.scope_ !== e) return n;
  if (!r.modified_) return it(e, r.base_, !0), r.base_;
  if (!r.finalized_) {
    (r.finalized_ = !0), r.scope_.unfinalizedDrafts_--;
    let o = r.copy_,
      i = o,
      l = !1;
    r.type_ === 3 && ((i = new Set(o)), o.clear(), (l = !0)),
      $e(i, (u, a) => kr(e, r, o, u, a, t, l)),
      it(e, o, !1),
      t &&
        e.patches_ &&
        ve("Patches").generatePatches_(r, t, e.patches_, e.inversePatches_);
  }
  return r.copy_;
}
function kr(e, n, t, r, o, i, l) {
  if (Me(o)) {
    let u =
        i && n && n.type_ !== 3 && !qt(n.assigned_, r) ? i.concat(r) : void 0,
      a = ot(e, o, u);
    if ((zr(t, r, a), Me(a))) e.canAutoFreeze_ = !1;
    else return;
  } else l && t.add(o);
  if (de(o) && !ut(o)) {
    if (!e.immer_.autoFreeze_ && e.unfinalizedDrafts_ < 1) return;
    ot(e, o), (!n || !n.scope_.parent_) && it(e, o);
  }
}
function it(e, n, t = !1) {
  !e.parent_ && e.immer_.autoFreeze_ && e.canAutoFreeze_ && Ve(n, t);
}
function Qi(e, n) {
  let t = Array.isArray(e),
    r = {
      type_: t ? 1 : 0,
      scope_: n ? n.scope_ : rt(),
      modified_: !1,
      finalized_: !1,
      assigned_: {},
      parent_: n,
      base_: e,
      draft_: null,
      copy_: null,
      revoke_: null,
      isManual_: !1,
    },
    o = r,
    i = Qt;
  t && ((o = [r]), (i = ze));
  let { revoke: l, proxy: u } = Proxy.revocable(o, i);
  return (r.draft_ = u), (r.revoke_ = l), u;
}
var Qt = {
    get(e, n) {
      if (n === C) return e;
      let t = k(e);
      if (!qt(t, n)) return Zi(e, t, n);
      let r = t[n];
      return e.finalized_ || !de(r)
        ? r
        : r === jt(e.base_, n)
        ? (Kt(e), (e.copy_[n] = Ge(r, e)))
        : r;
    },
    has(e, n) {
      return n in k(e);
    },
    ownKeys(e) {
      return Reflect.ownKeys(k(e));
    },
    set(e, n, t) {
      let r = Gr(k(e), n);
      if (r?.set) return r.set.call(e.draft_, t), !0;
      if (!e.modified_) {
        let o = jt(k(e), n),
          i = o?.[C];
        if (i && i.base_ === t)
          return (e.copy_[n] = t), (e.assigned_[n] = !1), !0;
        if (qi(t, o) && (t !== void 0 || qt(e.base_, n))) return !0;
        Kt(e), ue(e);
      }
      return (
        (e.copy_[n] === t && (t !== void 0 || n in e.copy_)) ||
          (Number.isNaN(t) && Number.isNaN(e.copy_[n])) ||
          ((e.copy_[n] = t), (e.assigned_[n] = !0)),
        !0
      );
    },
    deleteProperty(e, n) {
      return (
        jt(e.base_, n) !== void 0 || n in e.base_
          ? ((e.assigned_[n] = !1), Kt(e), ue(e))
          : delete e.assigned_[n],
        e.copy_ && delete e.copy_[n],
        !0
      );
    },
    getOwnPropertyDescriptor(e, n) {
      let t = k(e),
        r = Reflect.getOwnPropertyDescriptor(t, n);
      return (
        r && {
          writable: !0,
          configurable: e.type_ !== 1 || n !== "length",
          enumerable: r.enumerable,
          value: t[n],
        }
      );
    },
    defineProperty() {
      Y(11);
    },
    getPrototypeOf(e) {
      return Fe(e.base_);
    },
    setPrototypeOf() {
      Y(12);
    },
  },
  ze = {};
$e(Qt, (e, n) => {
  ze[e] = function () {
    return (arguments[0] = arguments[0][0]), n.apply(this, arguments);
  };
});
ze.deleteProperty = function (e, n) {
  return ze.set.call(this, e, n, void 0);
};
ze.set = function (e, n, t) {
  return Qt.set.call(this, e[0], n, t, e[0]);
};
function jt(e, n) {
  let t = e[C];
  return (t ? k(t) : e)[n];
}
function Zi(e, n, t) {
  let r = Gr(n, t);
  return r ? ("value" in r ? r.value : r.get?.call(e.draft_)) : void 0;
}
function Gr(e, n) {
  if (!(n in e)) return;
  let t = Fe(e);
  for (; t; ) {
    let r = Object.getOwnPropertyDescriptor(t, n);
    if (r) return r;
    t = Fe(t);
  }
}
function ue(e) {
  e.modified_ || ((e.modified_ = !0), e.parent_ && ue(e.parent_));
}
function Kt(e) {
  e.copy_ || (e.copy_ = Wt(e.base_, e.scope_.immer_.useStrictShallowCopy_));
}
var el = class {
  constructor(e) {
    (this.autoFreeze_ = !0),
      (this.useStrictShallowCopy_ = !1),
      (this.produce = (n, t, r) => {
        if (typeof n == "function" && typeof t != "function") {
          let i = t;
          t = n;
          let l = this;
          return function (a = i, ...d) {
            return l.produce(a, (s) => t.call(this, s, ...d));
          };
        }
        typeof t != "function" && Y(6),
          r !== void 0 && typeof r != "function" && Y(7);
        let o;
        if (de(n)) {
          let i = Nr(this),
            l = Ge(n, void 0),
            u = !0;
          try {
            (o = t(l)), (u = !1);
          } finally {
            u ? Yt(i) : Jt(i);
          }
          return Ar(i, r), Pr(o, i);
        } else if (!n || typeof n != "object") {
          if (
            ((o = t(n)),
            o === void 0 && (o = n),
            o === Hr && (o = void 0),
            this.autoFreeze_ && Ve(o, !0),
            r)
          ) {
            let i = [],
              l = [];
            ve("Patches").generateReplacementPatches_(n, o, i, l), r(i, l);
          }
          return o;
        } else Y(1, n);
      }),
      (this.produceWithPatches = (n, t) => {
        if (typeof n == "function")
          return (l, ...u) => this.produceWithPatches(l, (a) => n(a, ...u));
        let r, o;
        return [
          this.produce(n, t, (l, u) => {
            (r = l), (o = u);
          }),
          r,
          o,
        ];
      }),
      typeof e?.autoFreeze == "boolean" && this.setAutoFreeze(e.autoFreeze),
      typeof e?.useStrictShallowCopy == "boolean" &&
        this.setUseStrictShallowCopy(e.useStrictShallowCopy);
  }
  createDraft(e) {
    de(e) || Y(8), Me(e) && (e = tl(e));
    let n = Nr(this),
      t = Ge(e, void 0);
    return (t[C].isManual_ = !0), Jt(n), t;
  }
  finishDraft(e, n) {
    let t = e && e[C];
    (!t || !t.isManual_) && Y(9);
    let { scope_: r } = t;
    return Ar(r, n), Pr(void 0, r);
  }
  setAutoFreeze(e) {
    this.autoFreeze_ = e;
  }
  setUseStrictShallowCopy(e) {
    this.useStrictShallowCopy_ = e;
  }
  applyPatches(e, n) {
    let t;
    for (t = n.length - 1; t >= 0; t--) {
      let o = n[t];
      if (o.path.length === 0 && o.op === "replace") {
        e = o.value;
        break;
      }
    }
    t > -1 && (n = n.slice(t + 1));
    let r = ve("Patches").applyPatches_;
    return Me(e) ? r(e, n) : this.produce(e, (o) => r(o, n));
  }
};
function Ge(e, n) {
  let t = st(e)
    ? ve("MapSet").proxyMap_(e, n)
    : at(e)
    ? ve("MapSet").proxySet_(e, n)
    : Qi(e, n);
  return (n ? n.scope_ : rt()).drafts_.push(t), t;
}
function tl(e) {
  return Me(e) || Y(10, e), Br(e);
}
function Br(e) {
  if (!de(e) || ut(e)) return e;
  let n = e[C],
    t;
  if (n) {
    if (!n.modified_) return n.base_;
    (n.finalized_ = !0), (t = Wt(e, n.scope_.immer_.useStrictShallowCopy_));
  } else t = Wt(e, !0);
  return (
    $e(t, (r, o) => {
      zr(t, r, Br(o));
    }),
    n && (n.finalized_ = !1),
    t
  );
}
function Ur() {
  class e extends Map {
    constructor(a, d) {
      super(),
        (this[C] = {
          type_: 2,
          parent_: d,
          scope_: d ? d.scope_ : rt(),
          modified_: !1,
          finalized_: !1,
          copy_: void 0,
          assigned_: void 0,
          base_: a,
          draft_: this,
          isManual_: !1,
          revoked_: !1,
        });
    }
    get size() {
      return k(this[C]).size;
    }
    has(a) {
      return k(this[C]).has(a);
    }
    set(a, d) {
      let s = this[C];
      return (
        l(s),
        (!k(s).has(a) || k(s).get(a) !== d) &&
          (t(s),
          ue(s),
          s.assigned_.set(a, !0),
          s.copy_.set(a, d),
          s.assigned_.set(a, !0)),
        this
      );
    }
    delete(a) {
      if (!this.has(a)) return !1;
      let d = this[C];
      return (
        l(d),
        t(d),
        ue(d),
        d.base_.has(a) ? d.assigned_.set(a, !1) : d.assigned_.delete(a),
        d.copy_.delete(a),
        !0
      );
    }
    clear() {
      let a = this[C];
      l(a),
        k(a).size &&
          (t(a),
          ue(a),
          (a.assigned_ = new Map()),
          $e(a.base_, (d) => {
            a.assigned_.set(d, !1);
          }),
          a.copy_.clear());
    }
    forEach(a, d) {
      let s = this[C];
      k(s).forEach((g, f, c) => {
        a.call(d, this.get(f), f, this);
      });
    }
    get(a) {
      let d = this[C];
      l(d);
      let s = k(d).get(a);
      if (d.finalized_ || !de(s) || s !== d.base_.get(a)) return s;
      let g = Ge(s, d);
      return t(d), d.copy_.set(a, g), g;
    }
    keys() {
      return k(this[C]).keys();
    }
    values() {
      let a = this.keys();
      return {
        [Symbol.iterator]: () => this.values(),
        next: () => {
          let d = a.next();
          return d.done ? d : { done: !1, value: this.get(d.value) };
        },
      };
    }
    entries() {
      let a = this.keys();
      return {
        [Symbol.iterator]: () => this.entries(),
        next: () => {
          let d = a.next();
          if (d.done) return d;
          let s = this.get(d.value);
          return { done: !1, value: [d.value, s] };
        },
      };
    }
    [Symbol.iterator]() {
      return this.entries();
    }
  }
  function n(u, a) {
    return new e(u, a);
  }
  function t(u) {
    u.copy_ || ((u.assigned_ = new Map()), (u.copy_ = new Map(u.base_)));
  }
  class r extends Set {
    constructor(a, d) {
      super(),
        (this[C] = {
          type_: 3,
          parent_: d,
          scope_: d ? d.scope_ : rt(),
          modified_: !1,
          finalized_: !1,
          copy_: void 0,
          base_: a,
          draft_: this,
          drafts_: new Map(),
          revoked_: !1,
          isManual_: !1,
        });
    }
    get size() {
      return k(this[C]).size;
    }
    has(a) {
      let d = this[C];
      return (
        l(d),
        d.copy_
          ? !!(
              d.copy_.has(a) ||
              (d.drafts_.has(a) && d.copy_.has(d.drafts_.get(a)))
            )
          : d.base_.has(a)
      );
    }
    add(a) {
      let d = this[C];
      return l(d), this.has(a) || (i(d), ue(d), d.copy_.add(a)), this;
    }
    delete(a) {
      if (!this.has(a)) return !1;
      let d = this[C];
      return (
        l(d),
        i(d),
        ue(d),
        d.copy_.delete(a) ||
          (d.drafts_.has(a) ? d.copy_.delete(d.drafts_.get(a)) : !1)
      );
    }
    clear() {
      let a = this[C];
      l(a), k(a).size && (i(a), ue(a), a.copy_.clear());
    }
    values() {
      let a = this[C];
      return l(a), i(a), a.copy_.values();
    }
    entries() {
      let a = this[C];
      return l(a), i(a), a.copy_.entries();
    }
    keys() {
      return this.values();
    }
    [Symbol.iterator]() {
      return this.values();
    }
    forEach(a, d) {
      let s = this.values(),
        g = s.next();
      for (; !g.done; ) a.call(d, g.value, g.value, this), (g = s.next());
    }
  }
  function o(u, a) {
    return new r(u, a);
  }
  function i(u) {
    u.copy_ ||
      ((u.copy_ = new Set()),
      u.base_.forEach((a) => {
        if (de(a)) {
          let d = Ge(a, u);
          u.drafts_.set(a, d), u.copy_.add(d);
        } else u.copy_.add(a);
      }));
  }
  function l(u) {
    u.revoked_ && Y(3, JSON.stringify(k(u)));
  }
  Xi("MapSet", { proxyMap_: n, proxySet_: o });
}
var U = new el(),
  jr = U.produce,
  Kl = U.produceWithPatches.bind(U),
  ql = U.setAutoFreeze.bind(U),
  Wl = U.setUseStrictShallowCopy.bind(U),
  Xl = U.applyPatches.bind(U),
  Yl = U.createDraft.bind(U),
  Jl = U.finishDraft.bind(U);
function dt(e) {
  var n = D(function () {
      return Ve(typeof e == "function" ? e() : e, !0);
    }),
    t = n[1];
  return [
    n[0],
    se(function (r) {
      t(typeof r == "function" ? jr(r) : Ve(r));
    }, []),
  ];
}
function nl(e, n, t, r, o) {
  window.Shiny.shinyapp.makeRequest(e, n, t, r, o);
}
function Kr({ method: e, args: n, blobs: t }) {
  return new Promise((r, o) => {
    nl(
      e,
      n,
      (i) => {
        r(i);
      },
      (i) => {
        o(i);
      },
      t
    );
  });
}
function qr({
  patchInfo: e,
  patches: n,
  onSuccess: t,
  onError: r,
  columns: o,
  setData: i,
  setCellEditMapAtLoc: l,
}) {
  let u = n.map((a) => ({
    row_index: a.rowIndex,
    column_index: a.columnIndex,
    value: a.value,
  }));
  Kr({ method: e.key, args: [u] })
    .then((a) => {
      if (!Array.isArray(a))
        throw new Error("Expected a response of a list of patches");
      for (let s of a)
        if (!("row_index" in s && "column_index" in s && "value" in s))
          throw new Error(
            "Expected list of patches containing `row_index`, `column_index`, and `value`"
          );
      a = a;
      let d = a.map((s) => ({
        rowIndex: s.row_index,
        columnIndex: s.column_index,
        value: s.value,
      }));
      i((s) => {
        d.forEach(({ rowIndex: g, columnIndex: f, value: c }) => {
          s[g][f] = c;
        });
      }),
        d.forEach(({ rowIndex: s, columnIndex: g, value: f }) => {
          l(s, g, (c) => {
            (c.value = f), (c.state = ye.EditSuccess), (c.errorTitle = void 0);
          });
        }),
        t(d);
    })
    .catch((a) => {
      n.forEach(({ rowIndex: d, columnIndex: s, value: g }) => {
        l(d, s, (f) => {
          (f.value = String(g)),
            (f.state = ye.EditFailure),
            (f.errorTitle = String(a));
        });
      }),
        r(a);
    });
}
var ye = {
    EditSaving: "EditSaving",
    EditSuccess: "EditSuccess",
    EditFailure: "EditFailure",
    Editing: "Editing",
    Ready: "Ready",
  },
  rl = {
    EditSaving: "cell-edit-saving",
    EditSuccess: "cell-edit-success",
    EditFailure: "cell-edit-failure",
    Editing: "cell-edit-editing",
    Ready: void 0,
  },
  en = (e) =>
    e !== null &&
    typeof e != "string" &&
    Object.prototype.hasOwnProperty.call(e, "isShinyHtml") &&
    e.isShinyHtml === !0,
  Zt = (e) => (en(e) ? e.obj.html : e),
  Wr = ({
    containerRef: e,
    rowId: n,
    cell: t,
    patchInfo: r,
    columns: o,
    coldefs: i,
    rowIndex: l,
    columnIndex: u,
    editCellsIsAllowed: a,
    getSortedRowModel: d,
    cellEditInfo: s,
    setData: g,
    setCellEditMapAtLoc: f,
  }) => {
    let c = t.getValue(),
      p = t.column.columnDef.meta.isHtmlColumn,
      m = s?.value ?? c,
      _ = s?.state ?? ye.Ready,
      v = s?.errorTitle,
      w = s?.isEditing ?? !1,
      x = s?.editValue ?? Zt(m),
      M = B(null),
      I = B(null),
      N = se(
        (
          { resetIsEditing: S = !1, resetEditValue: A = !1 } = {
            resetIsEditing: !0,
            resetEditValue: !0,
          }
        ) => {
          f(l, u, (K) => {
            S && (K.isEditing = !1), A && (K.editValue = void 0);
          });
        },
        [l, u, f]
      ),
      J = (S) => {
        S.key === "Escape" && (S.preventDefault(), N());
      },
      O = (S) => {
        if (S.key !== "Tab") return;
        S.preventDefault();
        let A = S.shiftKey,
          K = u;
        for (;;) {
          let H = K + (A ? -1 : 1);
          if (H < 0 || H >= i.length) return;
          if (((K = H), i[H].meta.isHtmlColumn !== !0)) break;
        }
        be(),
          f(l, K, (H) => {
            H.isEditing = !0;
          });
      },
      ce = (S) => {
        if (S.key !== "Enter") return;
        S.preventDefault();
        let A = S.shiftKey,
          K = d(),
          H = K.rows.findIndex((q) => q.id === n);
        if (H < 0) return;
        let Te = H + (A ? -1 : 1);
        if (Te < 0 || Te >= K.rows.length) return;
        be();
        let pt = K.rows[Te].index;
        f(pt, u, (q) => {
          q.isEditing = !0;
        });
      },
      Ie = (S) => {
        [J, ce, O].forEach((A) => A(S));
      },
      be = se(() => {
        if (
          (f(l, u, (S) => {
            S.errorTitle = void 0;
          }),
          `${Zt(m)}` == `${x}`)
        ) {
          N(),
            f(l, u, (S) => {
              S.state = _;
            });
          return;
        }
        N({ resetIsEditing: !0 }),
          f(l, u, (S) => {
            S.state = ye.EditSaving;
          }),
          qr({
            patchInfo: r,
            patches: [{ rowIndex: l, columnIndex: u, value: x }],
            onSuccess: (S) => {
              N({ resetEditValue: !0 });
            },
            onError: (S) => {},
            columns: o,
            setData: g,
            setCellEditMapAtLoc: f,
          });
      }, [f, l, u, m, x, N, r, o, g, _]);
    L(() => {
      w && I.current && (I.current.focus(), I.current.select());
    }, [w]),
      L(() => {
        if (!w || !I.current) return;
        let S = (A) => {
          A.target !== I.current && (be(), N());
        };
        return (
          document.body.addEventListener("click", S),
          () => {
            document.body.removeEventListener("click", S);
          }
        );
      }, [_, be, l, u, w, N]);
    function ct(S) {
      w && S.target.select();
    }
    function ft(S) {
      f(l, u, (A) => {
        A.editValue = S.target.value;
      });
    }
    let P,
      Q,
      gt = v,
      z,
      Se = (S) => {
        S && (z ? ((z += " "), (z += S)) : (z = S));
      };
    Se(rl[w ? ye.Editing : _]);
    let we = !1,
      Be = null;
    return (
      _ === ye.EditSaving
        ? (Q = b.createElement("em", null, x))
        : (w
            ? (Be = b.createElement("textarea", {
                value: String(x),
                onChange: ft,
                onFocus: ct,
                onKeyDown: Ie,
                ref: I,
              }))
            : a && !p
            ? (Se("cell-editable"),
              (P = (S) => {
                f(l, u, (A) => {
                  (A.isEditing = !0), (A.editValue = Zt(m));
                });
              }))
            : Se("cell-html"),
          en(m)
            ? (we = !0)
            : (Q = tt(t.column.columnDef.cell, t.getContext()))),
      L(() => {
        if (!M.current || !we || !en(m)) return;
        let S = JSON.parse(JSON.stringify(m.obj));
        window.Shiny.renderContentAsync(M.current, S);
        let A = M.current;
        return () => {
          window.Shiny.unbindAll(A), A.replaceChildren("");
        };
      }, [M, m, l, u, we]),
      b.createElement(
        "td",
        { ref: M, onClick: P, title: gt, className: z },
        Be,
        Q
      )
    );
  };
var Xr = () => {
    let [e, n] = dt(new Map());
    return (
      Ur(),
      {
        cellEditMap: e,
        setCellEditMap: n,
        setCellEditMapAtLoc: (r, o, i) => {
          n((l) => {
            let u = Yr(r, o),
              a = l.get(u) ?? {};
            i(a), l.set(u, a);
          });
        },
      }
    );
  },
  Yr = (e, n) => `[${e}, ${n}]`;
var Jr = (e, n, t) => {
  let r = Yr(n, t);
  return [e.get(r) ?? {}, r];
};
function Qr(e, n, t) {
  let r = Object.assign({ top: 0, right: 0, bottom: 0, left: 0 }, t),
    o = e,
    i = o.scrollTop + r.top,
    l = o.scrollLeft + r.left,
    u = i + o.clientHeight - r.top - r.bottom,
    a = l + o.clientWidth - r.left - r.right;
  for (let d = 0; d < n.length; d++) {
    let s = n[d],
      g = s.offsetTop,
      f = s.offsetLeft;
    if (g >= i && g <= u && f >= l && f <= a) return s;
  }
  return null;
}
function tn(e, n) {
  return document?.defaultView?.getComputedStyle(e, null)?.getPropertyValue(n);
}
var to = (e) => {
  let [n, t] = D(!1),
    { range: r, from: o, to: i, onRangeChange: l } = e;
  return b.createElement(ol, {
    range: r,
    value: [o, i],
    editing: n,
    onValueChange: (u) => l(...u),
    onFocus: () => t(!0),
    onBlur: () => t(!1),
  });
};
var ol = (e) => {
  let [n, t] = e.value,
    { editing: r, onFocus: o } = e,
    i = B(null),
    l = B(null);
  return b.createElement(
    "div",
    {
      onBlur: (u) => {
        if (!u.currentTarget.contains(u.relatedTarget)) return e.onBlur();
      },
      onFocus: () => o(),
      style: { display: "flex", gap: "0.5rem" },
    },
    b.createElement("input", {
      ref: i,
      className: `form-control form-control-sm ${
        i.current?.checkValidity() ? "" : "is-invalid"
      }`,
      style: { flex: "1 1 0", width: "0" },
      type: "number",
      placeholder: Zr(r, "Min", e.range()[0]),
      defaultValue: n,
      step: "any",
      onChange: (u) => {
        let a = eo(u.target.value);
        i.current.classList.toggle("is-invalid", !u.target.checkValidity()),
          e.onValueChange([a, t]);
      },
    }),
    b.createElement("input", {
      ref: l,
      className: `form-control form-control-sm ${
        l.current?.checkValidity() ? "" : "is-invalid"
      }`,
      style: { flex: "1 1 0", width: "0" },
      type: "number",
      placeholder: Zr(r, "Max", e.range()[1]),
      defaultValue: t,
      step: "any",
      onChange: (u) => {
        let a = eo(u.target.value);
        l.current.classList.toggle("is-invalid", !u.target.checkValidity()),
          e.onValueChange([n, a]);
      },
    })
  );
};
function Zr(e, n, t) {
  return e ? (typeof t > "u" ? n : `${n} (${t})`) : null;
}
function eo(e) {
  if (e !== "") return +e;
}
function no(e) {
  let [n, t] = D([]),
    r = e
      ? {
          getFilteredRowModel: br(),
          getFacetedRowModel: Sr(),
          getFacetedUniqueValues: wr(),
          getFacetedMinMaxValues: Cr(),
          filterFns: {
            substring: (o, i, l, u) => o.getValue(i).toString().includes(l),
          },
          onColumnFiltersChange: t,
        }
      : {};
  return {
    columnFilters: n,
    columnFiltersState: { columnFilters: n },
    filtersTableOptions: r,
    setColumnFilters: t,
  };
}
var ro = ({ header: e, className: n, ...t }) => {
  let r = e.column.columnDef.meta?.typeHint;
  if (r.type === "html") return null;
  if (r.type === "numeric") {
    let [o, i] = e.column.getFilterValue() ?? [void 0, void 0];
    return to({
      from: o,
      to: i,
      range: () => e.column.getFacetedMinMaxValues() ?? [void 0, void 0],
      onRangeChange: (u, a) => e.column.setFilterValue([u, a]),
    });
  }
  return b.createElement("input", {
    ...t,
    className: `form-control form-control-sm ${n}`,
    type: "text",
    onChange: (o) => e.column.setFilterValue(o.target.value),
  });
};
var j = class e {
  _set;
  static _empty = new e(new Set());
  constructor(n) {
    this._set = n;
  }
  static empty() {
    return this._empty;
  }
  static just(...n) {
    return this.empty().add(...n);
  }
  has(n) {
    return this._set.has(n);
  }
  add(...n) {
    let t = new Set(this._set.keys());
    for (let r of n) t.add(r);
    return new e(t);
  }
  toggle(n) {
    return this.has(n) ? this.delete(n) : this.add(n);
  }
  delete(n) {
    let t = new Set(this._set.keys());
    return t.delete(n), new e(t);
  }
  clear() {
    return e.empty();
  }
  [Symbol.iterator]() {
    return this._set[Symbol.iterator]();
  }
  toList() {
    return [...this._set.keys()];
  }
};
var ee = class e {
  static _NONE = "none";
  static _ROW_SINGLE = "single";
  static _ROW_MULTIPLE = "multiple";
  static _COL_SINGLE = "single";
  static _col_multiple = "multiple";
  static _RECT_REGION = "region";
  static _RECT_CELL = "cell";
  static _rowEnum = {
    NONE: e._NONE,
    SINGLE: e._ROW_SINGLE,
    MULTIPLE: e._ROW_MULTIPLE,
  };
  static _colEnum = {
    NONE: e._NONE,
    SINGLE: e._COL_SINGLE,
    MULTIPLE: e._col_multiple,
  };
  static _rectEnum = {
    NONE: e._NONE,
    REGION: e._RECT_REGION,
    CELL: e._RECT_CELL,
  };
  row;
  col;
  rect;
  constructor({ row: n, col: t, rect: r }) {
    if (!Object.values(e._rowEnum).includes(n))
      throw new Error(`Invalid row selection mode: ${n}`);
    if (!Object.values(e._colEnum).includes(t))
      throw new Error(`Invalid col selection mode: ${t}`);
    if (!Object.values(e._rectEnum).includes(r))
      throw new Error(`Invalid rect selection mode: ${r}`);
    (this.row = n), (this.col = t), (this.rect = r);
  }
  is_none() {
    return (
      this.row === e._rowEnum.NONE &&
      this.col === e._colEnum.NONE &&
      this.rect === e._rectEnum.NONE
    );
  }
};
function io(e) {
  return (
    e || (e = { row: "multiple", col: "none", rect: "none" }),
    new ee({ row: e.row, col: e.col, rect: e.rect })
  );
}
function lo(e, n, t, r) {
  let [o, i] = D(j.empty()),
    [l, u] = D(null),
    a = (s) => {
      if (e.is_none()) return;
      let g = s.currentTarget,
        f = n(g),
        c = il(e, r, o, s, f, l);
      c && (i(c.selection), c.anchor && (u(f), g.focus()), s.preventDefault());
    },
    d = (s) => {
      if (e.is_none()) return;
      let g = s.currentTarget,
        f = n(g),
        c = o.has(f);
      if (e.row === ee._rowEnum.SINGLE) {
        if (s.key === " " || s.key === "Enter")
          o.has(f) ? i(j.empty()) : i(j.just(f)), s.preventDefault();
        else if (s.key === "ArrowUp" || s.key === "ArrowDown") {
          let p = t(f, s.key === "ArrowUp" ? -1 : 1);
          p && (s.preventDefault(), c && i(j.just(p)));
        }
      } else
        e.row === ee._rowEnum.MULTIPLE &&
          (s.key === " " || s.key === "Enter"
            ? (i(o.toggle(f)), s.preventDefault())
            : (s.key === "ArrowUp" || s.key === "ArrowDown") &&
              t(f, s.key === "ArrowUp" ? -1 : 1) &&
              s.preventDefault());
    };
  return {
    has(s) {
      return o.has(s);
    },
    set(s, g) {
      i(g ? o.add(s) : o.delete(s));
    },
    setMultiple(s) {
      i(j.just(...s));
    },
    clear() {
      i(o.clear());
    },
    keys() {
      return o;
    },
    itemHandlers() {
      return { onMouseDown: a, onKeyDown: d };
    },
  };
}
var oo = /^mac/i.test(
  window.navigator.userAgentData?.platform ?? window.navigator.platform
);
function il(e, n, t, r, o, i) {
  let { shiftKey: l, altKey: u } = r,
    a = oo ? r.metaKey : r.ctrlKey;
  if ((oo ? r.ctrlKey : r.metaKey) || u || e.row === ee._rowEnum.NONE)
    return null;
  if (e.row === ee._rowEnum.SINGLE)
    return a && !l
      ? t.has(o)
        ? { selection: j.empty(), anchor: !0 }
        : { selection: j.just(o), anchor: !0 }
      : { selection: j.just(o), anchor: !0 };
  if (e.row === ee._rowEnum.MULTIPLE)
    if (l && a) {
      if (i !== null && n) {
        let s = n(i, o);
        return { selection: t.add(...s) };
      }
    } else {
      if (a) return { selection: t.toggle(o), anchor: !0 };
      if (l) {
        if (i !== null && n) {
          let s = n(i, o);
          return { selection: j.just(...s) };
        }
      } else return { selection: j.just(o), anchor: !0 };
    }
  else throw new Error(`Unsupported row selection mode: ${e.row}`);
  return null;
}
function so() {
  let [e, n] = D([]);
  return {
    sorting: e,
    sortState: { sorting: e },
    sortingTableOptions: { onSortingChange: n, getSortedRowModel: Er() },
    setSorting: n,
  };
}
var ao = {
    className: "sort-arrow",
    viewBox: [-1, -1, 2, 2].map((e) => e * 1.4).join(" "),
    width: "100%",
    height: "100%",
    style: { paddingLeft: "3px" },
  },
  uo = { stroke: "#333333", strokeWidth: "0.6", fill: "transparent" },
  ll = b.createElement(
    "svg",
    { xmlns: "http://www.w3.org/2000/svg", ...ao },
    b.createElement("path", {
      d: "M -1 0.5 L 0 -0.5 L 1 0.5",
      ...uo,
      strokeLinecap: "round",
    })
  ),
  sl = b.createElement(
    "svg",
    { xmlns: "http://www.w3.org/2000/svg", ...ao },
    b.createElement("path", {
      d: "M -1 -0.5 L 0 0.5 L 1 -0.5",
      ...uo,
      strokeLinecap: "round",
    })
  ),
  co = ({ direction: e }) => {
    if (!e) return null;
    if (e === "asc") return ll;
    if (e === "desc") return sl;
    throw new Error(`Unexpected sort direction: '${e}'`);
  };
var fo = `
/*
 *
 * # Variables
 *
 */
shiny-data-frame {
  --shiny-datagrid-font-size: 0.9em;
  --shiny-datagrid-padding-x: 0.5em;
  --shiny-datagrid-padding-y: 0.3em;
  --shiny-datagrid-padding: var(--shiny-datagrid-padding-y) var(--shiny-datagrid-padding-x);
  --shiny-datagrid-grid-header-bgcolor: var(--bs-light, #eee);
  --shiny-datagrid-grid-header-gridlines-color: var(--bs-border-color, #ccc);
  --shiny-datagrid-grid-header-gridlines-style: solid;
  --shiny-datagrid-grid-gridlines-color: var(--bs-border-color, #ccc);
  --shiny-datagrid-grid-gridlines-style: solid;
  --shiny-datagrid-table-header-bottom-border: 1px solid;
  --shiny-datagrid-table-top-border: 1px solid;
  --shiny-datagrid-table-bottom-border: 1px solid;
  --shiny-datagrid-grid-body-hover-bgcolor: var(--shiny-datagrid-grid-header-bgcolor);
  --shiny-datagrid-grid-body-selected-bgcolor: #b4d5fe;
  --shiny-datagrid-grid-body-selected-color: var(--bs-dark);
  --shiny-datagrid-table-cell-edit-success-border-color: color-mix(in srgb, var(--bs-success) 20%, transparent);
  --shiny-datagrid-table-cell-edit-success-border-style: var(--shiny-datagrid-grid-gridlines-style);
  --shiny-datagrid-table-cell-edit-success-bgcolor: color-mix(in srgb, var(--bs-success) 10%, transparent);
  --shiny-datagrid-table-cell-edit-failure-border-color: color-mix(in srgb, var(--bs-danger) 40%, transparent);
  --shiny-datagrid-table-cell-edit-failure-border-style: var(--shiny-datagrid-grid-gridlines-style);
  --shiny-datagrid-table-cell-edit-failure-bgcolor: color-mix(in srgb, var(--bs-danger) 10%, transparent);
  --shiny-datagrid-table-cell-edit-saving-color: var(--bs-gray-500);
  --shiny-datagrid-table-cell-edit-saving-font-style: italic;
}

/*
 *
 * # BASE STYLES
 *
 */
shiny-data-frame *,
shiny-data-frame *::before,
shiny-data-frame *::after {
  box-sizing: border-box;
}

shiny-data-frame .shiny-data-grid svg.sort-arrow {
  display: inline-block;
  width: 0.85em;
  height: 0.85em;
  margin-bottom: 0.15em;
}

shiny-data-frame .shiny-data-grid {
  max-width: 100%;
  height: auto;
}
shiny-data-frame .shiny-data-grid.scrolling {
  height: 500px;
}
shiny-data-frame .shiny-data-grid > table {
  border-collapse: separate;
  border-spacing: 0;
}
shiny-data-frame .shiny-data-grid > table > thead {
  position: sticky;
  top: 0;
}
shiny-data-frame .shiny-data-grid > table > thead > tr > th {
  text-align: left;
  white-space: nowrap;
}
shiny-data-frame .shiny-data-grid > table > thead > tr > th:focus-visible {
  outline: 5px auto Highlight;
  outline: 5px auto -webkit-focus-ring-color;
}
shiny-data-frame .shiny-data-grid > table.filtering > thead > tr:nth-last-child(2) > th {
  border-bottom: none;
}
shiny-data-frame .shiny-data-grid > table.filtering > thead > tr.filters > th {
  font-weight: unset;
  padding-top: 0;
  /* Slight boost to bottom padding */
  padding-bottom: var(--shiny-datagrid-padding-x);
}
shiny-data-frame .shiny-data-grid > table.filtering > thead > tr.filters > th > input {
  width: 100%;
}

shiny-data-frame .shiny-data-grid > .shiny-data-grid-summary {
  font-size: var(--shiny-datagrid-font-size);
  padding-top: 0.3em;
}

/*
 *
 * # DATATABLE STYLES
 *
 */
shiny-data-frame .shiny-data-grid.shiny-data-grid-table {
  border-top: var(--shiny-datagrid-table-top-border);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-table.scrolling {
  border-bottom: var(--shiny-datagrid-table-bottom-border);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-table > table > thead > tr:last-child > th {
  border-bottom: var(--shiny-datagrid-table-header-bottom-border);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-table > table > tbody > tr[aria-selected=true] {
  --shiny-datagrid-grid-gridlines-color: var(--shiny-datagrid-grid-body-selected-bgcolor);
  background-color: var(--shiny-datagrid-grid-body-selected-bgcolor);
  color: var(--shiny-datagrid-grid-body-selected-color);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-table > table > tbody > tr[aria-selected=true] td {
  background-color: var(--shiny-datagrid-grid-body-selected-bgcolor);
  color: var(--shiny-datagrid-grid-body-selected-color);
}

/*
 *
 * # GRID STYLES
 *
 */
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table {
  font-size: var(--shiny-datagrid-font-size);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > thead > tr > th,
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > thead > tr > td {
  background-color: var(--shiny-datagrid-grid-header-bgcolor);
  padding: var(--shiny-datagrid-padding);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > tbody > tr:focus-visible {
  outline: 5px auto Highlight;
  outline: 5px auto -webkit-focus-ring-color;
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > tbody > tr:hover {
  --shiny-datagrid-grid-gridlines-color: inherit;
  background-color: var(--shiny-datagrid-grid-body-hover-bgcolor);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > tbody > tr[aria-selected=true] {
  background-color: var(--shiny-datagrid-grid-body-selected-bgcolor);
  color: var(--shiny-datagrid-grid-body-selected-color);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > tbody > tr > td {
  padding: var(--shiny-datagrid-padding);
}

/* ## Grid borders */
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table {
  border-collapse: separate;
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > thead > tr:first-child > th {
  border-top-style: var(--shiny-datagrid-grid-gridlines-style);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > thead > tr > th {
  border: 1px var(--shiny-datagrid-grid-gridlines-style) var(--shiny-datagrid-grid-header-gridlines-color);
  border-top-style: none;
  border-left-style: none;
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > thead > tr > th:first-child {
  border-left-style: var(--shiny-datagrid-grid-gridlines-style);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > tbody > tr > td {
  border: 1px var(--shiny-datagrid-grid-gridlines-style) var(--shiny-datagrid-grid-gridlines-color);
  border-top-style: none;
  border-left-style: none;
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid > table > tbody > tr > td:first-child {
  border-left-style: var(--shiny-datagrid-grid-gridlines-style);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid.scrolling {
  border: var(--shiny-datagrid-grid-gridlines-style) 1px var(--shiny-datagrid-grid-header-gridlines-color);
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid.scrolling > table > thead > tr:first-child > th {
  border-top-style: none;
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid.scrolling > table > tbody > tr:last-child > td {
  border-bottom-style: none;
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid.scrolling > table > thead > tr > th:first-child,
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid.scrolling > table > tbody > tr > td:first-child {
  border-left-style: none;
}
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid.scrolling > table > thead > tr > th:last-child,
shiny-data-frame .shiny-data-grid.shiny-data-grid-grid.scrolling > table > tbody > tr > td:last-child {
  border-right-style: none;
}

/*
 *
 * # FILLING LAYOUT STYLES
 *
 */
/* Center the table when inside of a card */
.card-body shiny-data-frame .shiny-data-grid {
  margin-left: auto;
  margin-right: auto;
}

/* When .shiny-data-grid is not scrolling, the containers shouldn't flex */
shiny-data-frame:has(> div > .shiny-data-grid:not(.scrolling)) {
  flex: 0 0 auto;
}
shiny-data-frame > div:has(> .shiny-data-grid:not(.scrolling)) {
  flex: 0 0 auto;
}

/*
 *
 * # CELL EDITING STYLES
 *
 */
shiny-data-frame .shiny-data-grid > table > tbody > tr > td.cell-edit-editing {
  color: transparent;
  position: relative;
}
shiny-data-frame .shiny-data-grid > table > tbody > tr > td.cell-edit-editing :not(textarea) {
  visibility: hidden;
}
shiny-data-frame .shiny-data-grid > table > tbody > tr > td.cell-edit-editing > textarea {
  position: absolute;
  padding: var(--shiny-datagrid-padding);
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
  background-color: inherit;
  resize: none;
}

shiny-data-frame .shiny-data-grid > table > tbody > tr > td.cell-html {
  cursor: default;
}
shiny-data-frame .shiny-data-grid > table > tbody > tr > td.cell-editable {
  cursor: text;
}
shiny-data-frame .shiny-data-grid > table > tbody > tr > td.cell-edit-saving {
  color: var(--shiny-datagrid-table-cell-edit-saving-color);
  font-style: var(--shiny-datagrid-table-cell-edit-saving-font-style);
}
shiny-data-frame .shiny-data-grid > table > tbody > tr > td.cell-edit-failure {
  outline: 2px var(--shiny-datagrid-table-cell-edit-failure-border-style) var(--shiny-datagrid-table-cell-edit-failure-border-color);
  background-color: var(--shiny-datagrid-table-cell-edit-failure-bgcolor);
}`;
function go(e, n, t) {
  let [r, o] = D(0),
    i = b.useCallback(
      (u) => {
        o(-1), u.target === u.currentTarget && Qr(e, n(), t)?.focus();
      },
      [e, n, t]
    ),
    l = b.useCallback((u) => {
      o(0);
    }, []);
  return { containerTabIndex: r, containerHandlers: { onFocus: i, onBlur: l } };
}
function po(e, n, t, r, o) {
  return oe(() => {
    let i = e ?? !0;
    if (!i) return null;
    let l =
      typeof i == "string"
        ? i
        : "Viewing rows {start} through {end} of {total}";
    if (!n || t.length === 0 || !r) return null;
    let u = n.scrollTop + r.clientHeight,
      a = n.scrollTop + n.clientHeight,
      [d, s] = al(u, a, t, (p, m) => p.start + p.size / 2);
    if (d === null || s === null) return null;
    let g = t[d],
      f = t[s];
    if (g.index === 0 && f.index === o - 1) return null;
    let c = ul(l, g.index + 1, f.index + 1, o);
    return b.createElement("div", { className: "shiny-data-grid-summary" }, c);
  }, [e, n, t, r, o]);
}
function al(e, n, t, r) {
  let o = null,
    i = null;
  for (let l = 0; l < t.length; l++) {
    let u = t[l];
    if (o === null) r(u, !0) >= e && ((o = l), (i = l));
    else if (r(u, !1) <= n) i = l;
    else break;
  }
  return [o, i];
}
function ul(e, n, t, r) {
  return e.replace(/\{(start|end|total)\}/g, (o, i) =>
    i === "start" ? n + "" : i === "end" ? t + "" : i === "total" ? r + "" : o
  );
}
var dl = ({
  id: e,
  gridInfo: { payload: n, patchInfo: t, selectionModes: r },
  bgcolor: o,
}) => {
  let { columns: i, typeHints: l, data: u, options: a } = n,
    { width: d, height: s, fill: g, filters: f } = a,
    c = B(null),
    p = B(null),
    m = B(null),
    { cellEditMap: _, setCellEditMapAtLoc: v } = Xr(),
    w = a.editable === !0,
    x = oe(
      () =>
        i.map((E, F) => {
          let R = l?.[F],
            T = R?.type === "html",
            ie = T ? !1 : void 0;
          return {
            accessorFn: (fe, So) => fe[F],
            filterFn:
              R?.type === "numeric" ? "inNumberRange" : "includesString",
            header: E,
            meta: { colIndex: F, isHtmlColumn: T, typeHint: R },
            cell: ({ getValue: fe }) => fe(),
            enableSorting: ie,
          };
        }),
      [i, l]
    ),
    M = oe(() => u, [u]),
    [I, N] = dt(u),
    { sorting: J, sortState: O, sortingTableOptions: ce } = so(),
    {
      columnFilters: Ie,
      columnFiltersState: be,
      filtersTableOptions: ct,
    } = no(f),
    ft = {
      data: I,
      columns: x,
      state: { ...O, ...be },
      getCoreRowModel: vr(),
      ...ce,
      ...ct,
    },
    P = Rr(ft),
    Q = Tr({
      count: P.getFilteredRowModel().rows.length,
      getScrollElement: () => c.current,
      estimateSize: () => 31,
      paddingStart: p.current?.clientHeight ?? 0,
      scrollingDelay: 10,
    });
  re(() => {
    Q.scrollToOffset(0);
  }, [n, Q]);
  let gt = Q.getTotalSize(),
    z = Q.getVirtualItems(),
    Se =
      ((z.length > 0 && z?.[0]?.start) || 0) - (p.current?.clientHeight ?? 0),
    we = z.length > 0 ? gt - (z?.[z.length - 1]?.end || 0) : 0,
    Be = po(a.summary, c?.current, z, p.current, Q.options.count),
    S = a.style ?? "grid",
    A = S === "grid" ? "shiny-data-grid-grid" : "shiny-data-grid-table",
    K = S === "table" ? "table table-sm" : null,
    H = io(r),
    Te = !H.is_none(),
    pt = H.row !== ee._rowEnum.NONE,
    q = lo(
      H,
      (E) => E.dataset.key,
      (E, F) => {
        let R = P.getSortedRowModel(),
          T = R.rows.findIndex((fe) => fe.id === E);
        if (T < 0 || ((T += F), T < 0 || T >= R.rows.length)) return null;
        let ie = R.rows[T].id;
        return (
          Q.scrollToIndex(T),
          setTimeout(() => {
            c.current?.querySelector(`[data-key='${ie}']`)?.focus();
          }, 0),
          ie
        );
      },
      (E, F) => cl(P.getSortedRowModel(), E, F)
    );
  L(() => {
    let E = (R) => {
      let T = R.detail.cellSelection;
      if (T.type === "none") {
        q.clear();
        return;
      } else if (T.type === "row") {
        q.setMultiple(T.rows.map(String));
        return;
      } else console.error("Unhandled cell selection update:", T);
    };
    if (!e) return;
    let F = document.getElementById(e);
    if (F)
      return (
        F.addEventListener("updateCellSelection", E),
        () => {
          F.removeEventListener("updateCellSelection", E);
        }
      );
  }, [e, q, u]),
    L(() => {
      if (!e) return;
      let E = `${e}_cell_selection`,
        F = null;
      if (H.is_none()) F = null;
      else if (H.row !== ee._rowEnum.NONE) {
        let R = q.keys().toList(),
          T = P.getSortedRowModel().rowsById;
        F = { type: "row", rows: R.map((ie) => T[ie].index).sort() };
      } else console.error("Unhandled row selection mode:", H);
      Shiny.setInputValue(E, F);
    }, [e, q, H, P, P.getSortedRowModel]),
    L(() => {
      if (!e) return;
      let E = `${e}_column_sort`;
      Shiny.setInputValue(E, J);
    }, [e, J]),
    L(() => {
      if (!e) return;
      let E = `${e}_column_filter`;
      Shiny.setInputValue(E, Ie);
    }, [e, Ie]),
    L(() => {
      if (!e) return;
      let E = `${e}_data_view_indices`,
        F = P.getSortedRowModel(),
        R = P.getSortedRowModel().rows.map((T) => T.index);
      Shiny.setInputValue(E, R);
    }, [e, P, J, Ie]),
    w &&
      Te &&
      console.error(
        "Should not have editable and row selection at the same time"
      );
  let ho = b.useCallback(
      () => m.current.querySelectorAll("[tabindex='-1']"),
      [m.current]
    ),
    on = go(c.current, ho, { top: p.current?.clientHeight ?? 0 });
  L(
    () => () => {
      P.resetSorting(), q.clear();
    },
    [n]
  );
  let vo = P.getHeaderGroups().length,
    ln = u.length > 0 ? "scrolling" : "",
    sn = c.current?.scrollHeight,
    an = c.current?.clientHeight;
  sn && an && sn <= an && (ln = "");
  let yo = (E) => (F) => {
      (F.key === " " || F.key === "Enter") &&
        E.toggleSorting(void 0, F.shiftKey);
    },
    bo = fl(Q),
    un = `shiny-data-grid ${A} ${ln}`;
  return (
    g && (un += " html-fill-item"),
    b.createElement(
      b.Fragment,
      null,
      b.createElement(
        "div",
        {
          className: un,
          ref: c,
          style: { width: d, height: s, overflow: "auto" },
        },
        b.createElement(
          "table",
          {
            className: K + (f ? " filtering" : ""),
            "aria-rowcount": I.length,
            "aria-multiselectable": pt,
            style: { width: d === null || d === "auto" ? void 0 : "100%" },
          },
          b.createElement(
            "thead",
            { ref: p, style: { backgroundColor: o } },
            P.getHeaderGroups().map((E, F) =>
              b.createElement(
                "tr",
                { key: E.id, "aria-rowindex": F + 1 },
                E.headers.map((R) => {
                  let T = R.isPlaceholder
                    ? void 0
                    : b.createElement(
                        "div",
                        {
                          style: {
                            cursor: R.column.getCanSort() ? "pointer" : void 0,
                            userSelect: R.column.getCanSort() ? "none" : void 0,
                          },
                        },
                        tt(R.column.columnDef.header, R.getContext()),
                        b.createElement(co, {
                          direction: R.column.getIsSorted(),
                        })
                      );
                  return b.createElement(
                    "th",
                    {
                      key: R.id,
                      colSpan: R.colSpan,
                      style: { width: R.getSize() },
                      scope: "col",
                      tabIndex: 0,
                      onClick: R.column.getToggleSortingHandler(),
                      onKeyDown: yo(R.column),
                    },
                    T
                  );
                })
              )
            ),
            f &&
              b.createElement(
                "tr",
                { className: "filters" },
                P.getFlatHeaders().map((E) =>
                  b.createElement(
                    "th",
                    { key: `filter-${E.id}` },
                    b.createElement(ro, { header: E })
                  )
                )
              )
          ),
          b.createElement(
            "tbody",
            { ref: m, tabIndex: on.containerTabIndex, ...on.containerHandlers },
            Se > 0 && b.createElement("tr", { style: { height: `${Se}px` } }),
            z.map((E) => {
              let F = P.getRowModel().rows[E.index];
              return (
                F &&
                b.createElement(
                  "tr",
                  {
                    key: E.key,
                    "data-index": E.index,
                    "aria-rowindex": E.index + vo,
                    "data-key": F.id,
                    ref: bo,
                    "aria-selected": q.has(F.id),
                    tabIndex: -1,
                    ...q.itemHandlers(),
                  },
                  F.getVisibleCells().map((R) => {
                    let T = R.row.index,
                      ie = R.column.columnDef.meta.colIndex,
                      [fe, So] = Jr(_, T, ie);
                    return b.createElement(Wr, {
                      key: R.id,
                      rowId: R.row.id,
                      containerRef: c,
                      cell: R,
                      patchInfo: t,
                      editCellsIsAllowed: w,
                      columns: i,
                      coldefs: x,
                      rowIndex: T,
                      columnIndex: ie,
                      getSortedRowModel: P.getSortedRowModel,
                      cellEditInfo: fe,
                      setData: N,
                      setCellEditMapAtLoc: v,
                    });
                  })
                )
              );
            }),
            we > 0 && b.createElement("tr", { style: { height: `${we}px` } })
          )
        )
      ),
      Be
    )
  );
};
function cl(e, n, t) {
  let r = e.rows.findIndex((l) => l.id === n),
    o = e.rows.findIndex((l) => l.id === t);
  if (r < 0 || o < 0) return [];
  r > o && ([r, o] = [o, r]);
  let i = [];
  for (let l = r; l <= o; l++) i.push(e.rows[l].id);
  return i;
}
function fl(e) {
  let n = B([]),
    t = se(
      (r) => {
        r && (r.isConnected ? e.measureElement(r) : n.current.push(r));
      },
      [e]
    );
  return (
    re(() => {
      n.current.length > 0 && n.current.splice(0).forEach(e.measureElement);
    }),
    t
  );
}
var nn = class extends Shiny.OutputBinding {
  find(n) {
    return $(n).find("shiny-data-frame");
  }
  renderValue(n, t) {
    n.renderValue(t);
  }
  renderError(n, t) {
    n.classList.add("shiny-output-error"), n.renderError(t);
  }
  clearError(n) {
    n.classList.remove("shiny-output-error"), n.clearError();
  }
};
Shiny.outputBindings.register(new nn(), "shinyDataFrame");
function mo(e) {
  if (!e) return;
  let n = tn(e, "background-color");
  if (!n) return n;
  let t = n.match(
    /^rgba\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\)$/
  );
  if (n === "transparent" || (t && parseFloat(t[4]) === 0)) {
    let r = tn(e, "background-image");
    return r && r !== "none" ? void 0 : mo(e.parentElement);
  }
  return n;
}
var _o = document.createElement("template");
_o.innerHTML = `<style>${fo}</style>`;
var rn = class extends HTMLElement {
  reactRoot;
  errorRoot;
  connectedCallback() {
    let [n] = [this];
    n.appendChild(_o.content.cloneNode(!0)),
      (this.errorRoot = document.createElement("span")),
      n.appendChild(this.errorRoot);
    let t = document.createElement("div");
    t.classList.add("html-fill-container", "html-fill-item"),
      n.appendChild(t),
      (this.reactRoot = Dr(t));
    let r = this.querySelector("script.data");
    if (r) {
      let o = JSON.parse(r.innerText);
      this.renderValue(o);
    }
  }
  renderValue(n) {
    if ((this.clearError(), !n)) {
      this.reactRoot.render(null);
      return;
    }
    this.reactRoot.render(
      b.createElement(
        Vt,
        null,
        b.createElement(dl, { id: this.id, gridInfo: n, bgcolor: mo(this) })
      )
    );
  }
  renderError(n) {
    this.reactRoot.render(null), (this.errorRoot.innerText = n.message);
  }
  clearError() {
    this.reactRoot.render(null), (this.errorRoot.innerText = "");
  }
};
customElements.define("shiny-data-frame", rn);
$(function () {
  Shiny.addCustomMessageHandler("shinyDataFrameMessage", function (e) {
    let n = new CustomEvent(e.handler, { detail: e.obj });
    document.getElementById(e.id)?.dispatchEvent(n);
  });
});
export { rn as ShinyDataFrameOutput };
/*! Bundled license information:

@tanstack/table-core/build/lib/index.mjs:
  (**
   * table-core
   *
   * Copyright (c) TanStack
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE.md file in the root directory of this source tree.
   *
   * @license MIT
   *)

@tanstack/react-table/build/lib/index.mjs:
  (**
   * react-table
   *
   * Copyright (c) TanStack
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE.md file in the root directory of this source tree.
   *
   * @license MIT
   *)

@tanstack/react-virtual/build/lib/_virtual/_rollupPluginBabelHelpers.mjs:
  (**
   * react-virtual
   *
   * Copyright (c) TanStack
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE.md file in the root directory of this source tree.
   *
   * @license MIT
   *)

@tanstack/virtual-core/build/lib/_virtual/_rollupPluginBabelHelpers.mjs:
  (**
   * virtual-core
   *
   * Copyright (c) TanStack
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE.md file in the root directory of this source tree.
   *
   * @license MIT
   *)

@tanstack/virtual-core/build/lib/utils.mjs:
  (**
   * virtual-core
   *
   * Copyright (c) TanStack
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE.md file in the root directory of this source tree.
   *
   * @license MIT
   *)

@tanstack/virtual-core/build/lib/index.mjs:
  (**
   * virtual-core
   *
   * Copyright (c) TanStack
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE.md file in the root directory of this source tree.
   *
   * @license MIT
   *)

@tanstack/react-virtual/build/lib/index.mjs:
  (**
   * react-virtual
   *
   * Copyright (c) TanStack
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE.md file in the root directory of this source tree.
   *
   * @license MIT
   *)
*/
//# sourceMappingURL=data-frame.js.map
