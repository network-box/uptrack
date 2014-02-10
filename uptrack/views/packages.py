def mark_downstream(request):
    try:
        pkg = request.context
        pkg.downstream = True

        return {"msg": "Marked %s as downstream-only in %s" % (pkg.name,
                                                               pkg.distro.name)}

    except Exception as e:
        return {"error": "%s" % e}
