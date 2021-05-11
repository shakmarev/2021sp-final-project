from final.canvas import get_canvas_parameters, pset_submission

if __name__ == "__main__":  # pragma: no cover
    repo, url, assignment = get_canvas_parameters()
    with pset_submission(repo, url, assignment) as ps:
        print(ps)
