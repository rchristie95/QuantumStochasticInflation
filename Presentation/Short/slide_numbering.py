"""Shared slide boundaries: reveals on the same canvas share one number."""
from pathlib import Path
import json
import re

SLIDE_STARTS = (
    'Title page', 'Talk outline', 'Classical theory / chapter',
    'Gradients and separate regions', 'What stochastic inflation does',
    'Phase-space Langevin dynamics', 'The light-field slow-roll limit',
    'Toy model / chapter', 'Average coordinate and total momentum',
    'Add one fresh oscillator', 'A canonical and unitary redefinition',
    'Product inputs become entangled outputs',
    'Measuring vs discarding the decoupled mode', 'Fock and position records',
    'Oscillator trajectories: n=1', 'Quantum stochastic inflation / chapter',
    'Canonical coarse-grained field variables', 'The homogeneous patch Hamiltonian',
    'Bulk and boundary shell', 'The single boundary-adapted channel',
    'The short-time joint state', 'One quantum channel',
    'Back to the boundary channel', 'Field POVM: read one decoupled quadrature',
    'Massive spectator drift', 'Mass-dependent Wigner dynamics',
    'Thanks for listening',
)


def slide_map():
    plan = json.loads(Path(__file__).with_name('reveal_plan.json').read_text())
    titles = [t for anchor in plan['original_topic_order']
              for t in plan['reveal_sequences'][anchor]]
    assert [t for t in titles if t in SLIDE_STARTS] == list(SLIDE_STARTS)
    number = 0
    result = {}
    for title in titles:
        if title in SLIDE_STARTS:
            number += 1
        result[title] = number
    return result


def number_script(script):
    """Keep authored prose verbatim, with one heading and time range per slide."""
    pattern = re.compile(r'^SHORT ACTION \d+ \| ([^|]+) \| (.+)$', re.M)
    matches = list(pattern.finditer(script))
    mapping = slide_map()
    assert [m[2] for m in matches] == list(mapping), 'Script/storyboard order differs'
    header = script[:matches[0].start()]
    header = re.sub(r'\d+ actions;', f'{len(SLIDE_STARTS)} slides;', header)
    header = header.replace('three seconds per action', 'three seconds per advance')
    header = header.replace('Action 1 is the opening state. Press Right once for each subsequent action.',
        'Slide numbers match the presentation and stay fixed while content builds.\nAdvance with Right as you present each slide.')
    header = re.sub(r'^Trace preparation is short action .*\n',
        f'The Gaussian trace and reduced purity are on slide {mapping["Tracing the collective complement"]}.\n', header, flags=re.M)
    header = re.sub(r'^Long-action references below.*\n', '', header, flags=re.M)
    groups = []
    for index, match in enumerate(matches):
        title = match[2]
        number = mapping[title]
        if not groups or groups[-1]['number'] != number:
            groups.append(dict(number=number, title=title,
                               start=match[1].strip().split('–')[0], bodies=[]))
        groups[-1]['end'] = match[1].strip().split('–')[-1]
        end = matches[index + 1].start() if index + 1 < len(matches) else len(script)
        body = script[match.end():end].strip('\r\n')
        body = re.sub(r'^Long version action\(s\):[^\n]*\n', '', body)
        groups[-1]['bodies'].append(body)
    output = [header.rstrip(), '']
    for group in groups:
        output += [f"SHORT SLIDE {group['number']:03} | {group['start']}–{group['end']} | {group['title']}",
                   '', '\n\n'.join(group['bodies']), '']
    result = '\n'.join(output)
    # Exact preservation of all quoted narration, including manual edits.
    quoted = lambda s: re.findall(r'^".*"$', s, flags=re.M)
    assert quoted(result) == quoted(script)
    return result
