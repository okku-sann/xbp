#!/usr/bin/env ruby

require "pathname"
require "uri"

root = Pathname.new(Dir.pwd)
html_files = Dir.glob(root.join("**/*.html")).reject { |path| path.include?("/.git/") }
failures = []

external = /\A(?:https?:|mailto:|tel:|#|javascript:)/i

html_files.each do |file|
  html = File.read(file)
  html = html.gsub(/<pre\b[^>]*>.*?<\/pre>/mi, "")
  html.scan(/\b(?:href|src)=["']([^"']+)["']/i).flatten.each do |raw_value|
    value = raw_value.strip
    next if value.empty? || value.match?(external)

    local_path = URI.decode_www_form_component(value.split("#", 2).first.split("?", 2).first)
    next if local_path.empty?

    resolved = Pathname.new(File.expand_path(local_path, File.dirname(file)))
    unless resolved.to_s.start_with?(root.to_s) && resolved.exist?
      failures << "#{Pathname.new(file).relative_path_from(root)} -> #{value}"
    end
  end
end

unless failures.empty?
  warn "Missing local references:"
  failures.each { |failure| warn "- #{failure}" }
  exit 1
end

puts "Build check passed: #{html_files.length} HTML files checked."
