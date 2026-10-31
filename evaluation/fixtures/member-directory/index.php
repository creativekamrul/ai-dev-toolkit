<?php
declare(strict_types=1);
$members = [
    ['name' => 'Amira Khan', 'role' => 'Club coordinator', 'team' => 'Operations', 'email' => 'amira@example.com', 'since' => '2021'],
    ['name' => 'Daniel O’Neil', 'role' => 'Events lead', 'team' => 'Community', 'email' => 'daniel@example.com', 'since' => '2022'],
    ['name' => 'Leah Chen', 'role' => 'Design & communications', 'team' => 'Creative', 'email' => 'leah@example.com', 'since' => '2020'],
    ['name' => 'Rafi Ahmed', 'role' => 'Volunteer mentor', 'team' => 'Community', 'email' => 'rafi@example.com', 'since' => '2023'],
    ['name' => 'Sofia Martins', 'role' => 'Treasurer', 'team' => 'Operations', 'email' => 'sofia@example.com', 'since' => '2022'],
];
function e(string $value): string { return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
$raw = $_GET['q'] ?? '';
$error = !is_string($raw) ? 'Enter a single search phrase.' : (strlen($raw) > 200 ? 'Enter a shorter search phrase.' : '');
$query = is_string($raw) && $error === '' ? trim($raw) : '';
if ($error !== '') { http_response_code(400); }
$matches = $error !== '' ? [] : array_values(array_filter($members, static fn(array $member): bool => $query === '' || stripos(implode(' ', $member), $query) !== false));
?>
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Member directory · Northbank Club</title><link rel="stylesheet" href="style.css"></head>
<body><a class="skip" href="#main">Skip to directory</a><header><a href="./" class="brand"><b>N</b> NORTHBANK CLUB</a><span>Member services</span></header><main id="main"><p class="eyebrow">PEOPLE & COMMUNITY</p><div class="heading"><div><h1>Member directory</h1><p>Find the right person. Keep the club connected.</p></div><div class="total"><strong><?= count($members) ?></strong><span>club members</span></div></div>
<section class="search-panel" aria-label="Search members"><form method="get" action="index.php"><label for="q">Search by name, role, team or email</label><div class="search-row"><input id="q" name="q" type="search" value="<?= e($query) ?>" placeholder="e.g. Amira or Community"<?= $error !== '' ? ' aria-invalid="true" aria-describedby="error"' : '' ?>><button type="submit">Search directory</button><?php if ($query !== '' || $error !== ''): ?><a class="clear" href="index.php">Clear search</a><?php endif ?></div></form><?php if ($error !== ''): ?><p id="error" role="alert"><?= e($error) ?></p><?php endif ?></section>
<div class="result-heading"><h2><?= $error !== '' ? 'Search needs attention' : ($query === '' ? 'All members' : 'Search results') ?></h2><p><?= count($matches) ?> <?= count($matches) === 1 ? 'member' : 'members' ?><?= $query !== '' ? ' matching “' . e($query) . '”' : '' ?></p></div>
<?php if ($matches): ?><ul class="members"><?php foreach ($matches as $member): ?><li><div class="avatar" aria-hidden="true"><?= e(substr($member['name'], 0, 1)) ?></div><div class="identity"><h3><?= e($member['name']) ?></h3><p><?= e($member['role']) ?></p></div><span class="team"><?= e($member['team']) ?></span><div class="contact"><a href="mailto:<?= e($member['email']) ?>"><?= e($member['email']) ?></a><span>Member since <?= e($member['since']) ?></span></div></li><?php endforeach ?></ul><?php else: ?><div class="empty"><h3><?= $error !== '' ? 'Let’s try that search again.' : 'No members found.' ?></h3><p><?= $error !== '' ? 'Use a short text phrase in the search field above.' : 'Try a different name or team, or clear the search to see everyone.' ?></p><a href="index.php">View all members</a></div><?php endif ?>
<p class="note">Demo directory · Fictional people and example email addresses.</p></main><footer><span>NORTHBANK CLUB</span><span>A place to belong.</span></footer></body></html>
