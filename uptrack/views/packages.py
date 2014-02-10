def mark_downstream(request):
    try:
        pkg = request.context
        pkg.downstream = True

        return {"msg": "Marked %s as downstream-only in %s" % (pkg.name,
                                                               pkg.distro.name)}

    except Exception as e:
        return {"error": "%s" % e}

def unmark_downstream(request):
    try:
        pkg = request.context
        pkg.downstream = False

        return {"msg": "Unmarked %s as downstream-only in %s" % (pkg.name,
                                                                 pkg.distro.name)}

    except Exception as e:
        return {"error": "%s" % e}

def mark_renamed(request):
    try:
        upstream_pkgname = request.GET["upstream_pkgname"]

        if upstream_pkgname == "":
            upstream_pkgname = None

    except KeyError as e:
        return {"error": "Please provide an upstream name"}

    try:
        pkg = request.context
        pkg.upstream_pkgname = upstream_pkgname

        if upstream_pkgname is not None:
            msg = ("Marked %s as renamed from %s in %s"
                   % (pkg.name, upstream_pkgname, pkg.distro.name))

        else:
            msg = "Unmarked %s as renamed in %s" % (pkg.name, pkg.distro.name)

        return {"msg": msg}

    except Exception as e:
        return {"error": "%s" % e}
